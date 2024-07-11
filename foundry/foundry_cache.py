import logging
import os
import re

from concurrent.futures import ThreadPoolExecutor, as_completed
import h5py
from mdf_forge import Forge
import numpy as np
import pandas as pd
import shutil
from tqdm.auto import tqdm
from typing import List, Any, Tuple

from .https_download import recursive_ls, download_file
from foundry.jsonschema_models.project_model import Split as FoundrySplit
from foundry.models import FoundrySchema
from foundry.utils import _read_csv, _read_json, _read_excel, is_pandas_pytable

logger = logging.getLogger(__name__)


class FoundryCache():
    """The FoundryCache manages the local storage of FoundryDataset objects"""

    def __init__(self,
                 forge_client: Forge,
                 transfer_client: Any,
                 use_globus,
                 interval,
                 parallel_https,
                 verbose,
                 local_cache_dir: str = None):
        """
        Initializes a FoundryCache object.

        Args:
            forge_client (Forge): The Forge client object.
            transfer_client (Any): The transfer client object.
            use_globus (bool): Flag indicating whether to use Globus for downloading.
            interval (int): How often to wait before checking Globus transfer status.
            parallel_https (int): Number of threads to use for downloading via HTTP.
            verbose (bool): Flag indicating whether to produce more debug messages.
            local_cache_dir (str, optional): The local cache directory. Defaults to None.
                If not specified, defaults to either the environmental variable 'FOUNDRY_LOCAL_CACHE_DIR'
                or './data/'.
        """
        if local_cache_dir:
            self.local_cache_dir = local_cache_dir
        else:
            self.local_cache_dir = os.environ.get("FOUNDRY_LOCAL_CACHE_DIR", './data/')
        self.forge_client = forge_client
        self.transfer_client = transfer_client
        self.use_globus = use_globus
        self.interval = interval
        self.parallel_https = parallel_https
        self.verbose = verbose

    def download_to_cache(self,
                          dataset_name: str,
                          splits: List[FoundrySplit] = None):
        """
        Checks if the data is downloaded, and if not, downloads the data from source to local storage.

        Args:
            dataset_name (str): Name of the dataset (equivalent to source_id in MDF).
            splits (List[FoundrySplit], optional): List of splits in the dataset. Defaults to None.

        Returns:
            FoundryCache: The FoundryCache object.
        """
        if not self.validate_local_dataset_storage(dataset_name, splits):
            if self.use_globus:
                self.download_via_globus(dataset_name)
            else:
                self.download_via_http(dataset_name)

        self.validate_local_dataset_storage(dataset_name, splits)

        return self

    def download_via_globus(self,
                            dataset_name: str):
        """
        Downloads selected dataset over Globus.

        Args:
            dataset_name (str): Name of the dataset (equivalent to source_id in MDF).
        """
        # query for mdf data representation
        res = self.forge_client.search(
            f"mdf.source_id:{dataset_name}", advanced=True
        )

        self.forge_client.globus_download(
            res,
            dest=self.local_cache_dir,
            interval=self.interval,
            download_datasets=True,
        )

    def download_via_http(self, dataset_name: str):
        """
        Downloads selected dataset from MDF over HTTP.
        Args:
        dataset_name (str): Name of the dataset (equivalent to source_id in MDF).
        """
        https_config = {
            "source_ep_id": "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec",
            "base_url": "https://data.materialsdatafacility.org",
            "folder_to_crawl": f"/foundry/{dataset_name}/",
            "source_id": dataset_name
        }

        # Begin finding files to download
        task_generator = recursive_ls(self.transfer_client,
                                      https_config['source_ep_id'],
                                      https_config['folder_to_crawl'])

        with ThreadPoolExecutor(self.parallel_https) as executor:
            # First submit all files
            futures = [executor.submit(download_file, f, self.local_cache_dir, https_config)
                       for f in tqdm(task_generator, disable=not self.verbose, desc="Finding files")]
            # Check that they completed successfully
            for result in tqdm(as_completed(futures), disable=not self.verbose, desc="Downloading files"):
                if result.exception() is not None:
                    for f in futures:
                        f.cancel()
                    raise result.exception()

    def validate_local_dataset_storage(self,
                                       dataset_name: str,
                                       splits: List[FoundrySplit] = None):
        """
        Verifies that the local storage location exists and all expected files are present.

        Args:
            dataset_name (str): Name of the dataset (equivalent to source_id in MDF).
            splits (List[FoundrySplit], optional): Labels of splits to be loaded. Defaults to None.

        Returns:
            bool: True if the dataset exists and contains all the desired files; False otherwise.
        """
        path = os.path.join(self.local_cache_dir, dataset_name)

        # after download check making sure directory exists, contains all indicated files
        if os.path.isdir(path):
            # checking all necessary files are present
            if splits:
                missing_files = []
                for split in splits:
                    if split.path[0] == '/':  # if absolute path, make it a relative path
                        split.path = split.path[1:]
                    if not os.path.isfile(os.path.join(path, split.path)):
                        # keeping track of all files not downloaded
                        missing_files.append(split.path)
                if len(missing_files) > 0:
                    logger.debug('Dataset is not complete')
                    return False
                else:
                    logger.debug("Dataset has already been downloaded and contains all the desired files")
                    return True
            else:
                if len(os.listdir(path)) >= 1:
                    logger.info("Dataset has already been downloaded and contains all the desired files")
                    return True
                else:
                    logger.debug('Dataset is not complete')
                    return False
        else:
            logger.debug('Dataset is not present')
            return False

    def _repr_html_(self):
        return f"""
        <div>
            <h3>FoundryCache</h3>
            <ul>
                <li>Local Cache Directory: {self.local_cache_dir}</li>
                <li>Use Globus: {self.use_globus}</li>
                <li>Interval: {self.interval}</li>
                <li>Parallel HTTPS: {self.parallel_https}</li>
                <li>Verbose: {self.verbose}</li>
            </ul>
        </div>
        """

    def load_as_dict(self,
                     split: str,
                     dataset_name: str,
                     foundry_schema: FoundrySchema,
                     as_hdf5: bool):
        """
        Load the data associated with the specified dataset and return it as a labeled dictionary of tuples.

        Args:
            split (str): Split to load the data from.
            dataset_name (str): Name of the dataset (equivalent to source_id in MDF).
            foundry_schema (FoundrySchema, optional): FoundrySchema object. Defaults to None.
            as_hdf5 (bool, optional): If True and dataset is in HDF5 format, keep data in HDF5 format. Defaults to False.

        Returns:
            dict: A labeled dictionary of tuples containing the loaded data.
        """
        # Ensure local copy of data is available
        self.download_to_cache(dataset_name,
                               foundry_schema.splits)

        data = {}

        # Handle splits if they exist. Return as a labeled dictionary of tuples
        try:
            if hasattr(foundry_schema, 'splits'):
                for split in foundry_schema.splits:
                    data[split.label] = self._load_data(foundry_schema=foundry_schema,
                                                        file=split.path,
                                                        source_id=dataset_name,
                                                        as_hdf5=as_hdf5)
                return data
            else:
                return {"data": self._load_data(foundry_schema=foundry_schema,
                                                source_id=dataset_name,
                                                as_hdf5=as_hdf5)}
        except Exception as e:
            raise Exception(
                "FoundryDataset not loaded!") from e

    def load_as_torch(self,
                      split: str,
                      dataset_name: str,
                      foundry_schema: FoundrySchema,
                      as_hdf5: bool):
        """Convert Foundry Dataset to a PyTorch Dataset

        Arguments:
            split (string): Split to create PyTorch Dataset on.
                    **Default:** ``None``

        Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split

        """
        # Ensure local copy of data is available
        self.download_to_cache(dataset_name,
                               foundry_schema.splits,
                               self.use_globus,
                               self.interval,
                               self.parallel_https,
                               self.verbose,
                               self.transfer_client)

        from foundry.loaders.torch_wrapper import TorchDataset

        inputs, targets = self._get_inputs_targets(split)
        return TorchDataset(inputs, targets)

    def load_as_tensorflow(self,
                           split: str,
                           dataset_name: str,
                           foundry_schema: FoundrySchema,
                           as_hdf5: bool):
        """Convert Foundry Dataset to a Tensorflow Sequence

        Arguments:
            split (string): Split to create Tensorflow Sequence on.
                    **Default:** ``None``

        Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split

        """

        # Ensure local copy of data is available
        self.download_to_cache(dataset_name,
                               foundry_schema.splits,
                               self.use_globus,
                               self.interval,
                               self.parallel_https,
                               self.verbose,
                               self.transfer_client)

        from foundry.loaders.tf_wrapper import TensorflowSequence

        inputs, targets = self._get_inputs_targets(split)
        return TensorflowSequence(inputs, targets)

    def _get_inputs_targets(self, split: str = None):
        """Get Inputs and Outputs from a Foundry Dataset

        Helper function for loading the data from files into memory in various forms.

        Arguments:
            split (string): Split to get inputs and outputs from.
                    **Default:** ``None``

        Returns: (Tuple) Tuple of the inputs and outputs
        """
        raw = self.load_data(as_hdf5=False)

        if not split:
            split = self.dataset.splits[0].type

        if self.dataset.data_type == "hdf5":
            inputs = []
            targets = []
            for key in self.dataset.keys:
                if len(raw[split][key.type][key.key[0]].keys()) != self.dataset.n_items:
                    continue

                # Get a numpy array of all the values for each item for that key
                val = np.array([raw[split][key.type][key.key[0]][k] for k in raw[split][key.type][key.key[0]].keys()])
                if key.type == 'input':
                    inputs.append(val)
                else:
                    targets.append(val)

            return (inputs, targets)

        elif self.dataset.data_type == "tabular":
            inputs = []
            targets = []

            for index, arr in enumerate([inputs, targets]):
                df = raw[split][index]
                for key in df.keys():
                    arr.append(df[key].values)

            return (inputs, targets)

        else:
            raise NotImplementedError

    def _load_data(self,
                   foundry_schema: FoundrySchema,
                   file: str = "foundry_dataframe.json",
                   source_id: str = None,
                   as_hdf5: bool = False) -> Tuple[Any, Any]:
        """
        Load the data from the cached file.
        Args:
        foundry_schema (FoundrySchema): The FoundrySchema object.
        file (str, optional): The name of the file to load. Defaults to "foundry_dataframe.json".
        source_id (str, optional): The source ID of the dataset. Defaults to None.
        as_hdf5 (bool, optional): If True, keep data in HDF5 format if the dataset is in HDF5 format. Defaults to False.
        Returns:
        tuple: A tuple containing the input and target data.
        """
        # Build the path to access the cached data
        path = os.path.join(self.local_cache_dir, source_id)
        if path is None:
            raise ValueError(f"Path to data file is invalid; check that dataset source_id is valid: "
                             f"{source_id or self.mdf['source_id']}")

        # Check for version folders
        version_folders = [d for d in os.listdir(path) if re.match(r'\d+\.\d+', d)]
        if version_folders:
            # Sort version folders and get the latest one
            latest_version = sorted(version_folders, key=lambda x: [int(n) for n in x.split('.')], reverse=True)[0]
            path = os.path.join(path, latest_version)
            print(f"Loading from version folder: {latest_version}")

        path_to_file = os.path.join(path, file)

        # Check to see whether file exists at path
        if not os.path.isfile(path_to_file):
            raise FileNotFoundError(f"No file found at expected path: {path_to_file}")

        # Handle Foundry-defined types.
        if foundry_schema.data_type == "tabular":
            # TODO: Add hashes and versioning to metadata and checking to the file
            read_fns = [(_read_json, {"lines": False, "path_to_file": path_to_file}),
                        (_read_json, {"lines": True, "path_to_file": path_to_file}),
                        (_read_csv, {"path_to_file": path_to_file}),
                        (_read_excel, {"path_to_file": path_to_file})]
            dataframe = None
            for fn, params in read_fns:
                try:
                    dataframe = fn(**params)
                except Exception as e:
                    logger.info(f"Unable to read file with {fn.__name__} with params {params}: {e}")
                if dataframe is not None:
                    logger.info(f"Succeeded with {fn.__name__} with params {params}")
                    break
            if dataframe is None:
                logger.fatal(f"Cannot read {path_to_file} as tabular data, failed to load")
                raise ValueError(f"Cannot read tabular data from {path_to_file}")
            return (
                dataframe[self.get_keys(foundry_schema, "input")],
                dataframe[self.get_keys(foundry_schema, "target")],
            )
        elif foundry_schema.data_type == "hdf5":
            f = h5py.File(path_to_file, "r")
            special_types = ["input", "target"]
            tmp_data = {s: {} for s in special_types}
            for s in special_types:
                for key in self.get_keys(foundry_schema, s):
                    if as_hdf5:
                        tmp_data[s][key] = f[key]
                    elif isinstance(f[key], h5py.Group):
                        if is_pandas_pytable(f[key]):
                            df = pd.read_hdf(path_to_file, key)
                            tmp_data[s][key] = df
                        else:
                            tmp_data[s][key] = f[key]
                    elif isinstance(f[key], h5py.Dataset):
                        tmp_data[s][key] = f[key][0:]
            return tmp_data
        else:
            raise NotImplementedError

    def get_keys(self,
                 foundry_schema: FoundrySchema,
                 type: str = None,
                 as_object: bool = False):
        """Get keys for a Foundry dataset

        Arguments:
            foundry_schema (FoundrySchema): The schema from MDF that contains the keys
            type (str): The type of key to be returned e.g., "input", "target"
            as_object (bool): When ``False``, will return a list of keys in as strings
                    When ``True``, will return the full key objects
                    **Default:** ``False``
        Returns: (list) String representations of keys or if ``as_object``
                    is False otherwise returns the full key objects.

        """

        if as_object:
            if type:
                return [key for key in foundry_schema.keys if key.type == type]
            else:
                return [key for key in foundry_schema.keys]

        else:
            if type:
                keys = [key.key for key in foundry_schema.keys if key.type == type]
            else:
                keys = [key.key for key in foundry_schema.keys]

            key_list = []
            for k in keys:
                key_list = key_list + k
            return key_list

    def clear_cache(self,
                    dataset_name: str = None):
        """Deletes all of the locally stored datasets

        Arguments:
            dataset_name (str): Optional name of a specific dataset. If omitted,
                                all datsets will be erased
        """
        if dataset_name:
            answer = input(f"This will delete the data for {dataset_name} - are you sure you want to continue? (y/n)")
            if answer.lower() in ["y", "yes"]:
                path = os.path.join(self.local_cache_dir, dataset_name)
            else:
                return
        else:
            answer = input(f"This will delete ALL of the data in {self.local_cache_dir} - are you sure you want to continue? (y/n)")
            if answer.lower() in ["y", "yes"]:
                path = self.local_cache_dir
            else:
                return
        if os.path.isdir(path):
            shutil.rmtree(path)
