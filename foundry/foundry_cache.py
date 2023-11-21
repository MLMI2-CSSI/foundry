import logging
import os

from concurrent.futures import ThreadPoolExecutor, as_completed
from mdf_forge import Forge
import shutil
from tqdm.auto import tqdm
from typing import List, Any

from foundry.https_download import recursive_ls, download_file
from foundry.models import FoundrySplit, FoundrySchema
from .utils import _read_csv, _read_json, _read_excel

logger = logging.getLogger(__name__)


class FoundryCache():
    """The FoundryCache manages the local storage of FoundryDataset objects"""

    def __init__(self, 
                 forge_client: Forge,
                 transfer_client: Any):

        self.local_cache_dir = os.environ.get("FOUNDRY_LOCAL_CACHE_DIR", "./data")
        self.forge_client = forge_client
        self.transfer_client = transfer_client

    def download_to_cache(self, 
                          dataset_name: str,
                          splits: List[FoundrySplit] = None, 
                          globus: bool = False, 
                          interval: int = 10, 
                          parallel_https: int = 4, 
                          verbose: bool = False,
                          transfer_client = None):
        """Downloads the data from source to local storage
        
        Args:
            dataset_name (str): name of dataset (equivalrnt to source_id in MDF)
            splits List[FoundrySplit]: list of splits in the dataset
            globus (bool): if True, use Globus to download the data else try HTTPS
            interval (int): How often to wait before checking Globus transfer status
            parallel_https (int): Number of files to download in parallel if using HTTPS
            verbose (bool): Produce more debug messages to screen

        """
        if not self.validate_local_dataset_storage(dataset_name, splits):
            if globus:
                self.download_via_globus(dataset_name, interval)
            else:
                self.download_via_http(dataset_name, parallel_https, verbose, self.transfer_client)

        self.validate_local_dataset_storage(dataset_name, splits)

        return self

    def download_via_globus(self, 
                            dataset_name: str, 
                            interval: int):
        """ Downloads selected dataset over globus

        Args:
            dataset_name (str): name of dataset (equivalent to source_id in MDF)
            interval (int): How often to wait before checking Globus transfer status

        """
        # query for mdf data representation
        res = self.forge_client.search(
            f"mdf.source_id:{dataset_name}", advanced=True
        )

        self.forge_client.globus_download(
            res,
            dest=self.local_cache_dir,
            interval=interval,
            download_datasets=True,
        )

    def download_via_http(self, 
                          dataset_name: str, 
                          parallel_https: int, 
                          verbose: bool,
                          transfer_client: Any):
        """Downloads selected dataset from MDF over http

        Args:
            dataset_name (str): name of dataset (equivalrnt to source_id in MDF)
            parallel_https (int): number of threads to use for downloading
            verbose (bool): Produce more debug messages to screen

        """
        https_config = {
            "source_ep_id": "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec",
            "base_url": "https://data.materialsdatafacility.org",
            "folder_to_crawl": f"/foundry/{dataset_name}/",
            "source_id": dataset_name
        }

        # Begin finding files to download
        task_generator = recursive_ls(transfer_client,
                                      https_config['source_ep_id'],
                                      https_config['folder_to_crawl'])
        with ThreadPoolExecutor(parallel_https) as executor:
            # First submit all files
            futures = [executor.submit(lambda x: download_file(x, https_config), f)
                       for f in tqdm(task_generator, disable=not verbose, desc="Finding files")]

            # Check that they completed successfully
            for result in tqdm(as_completed(futures), disable=not verbose, desc="Downloading files"):
                if result.exception() is not None:
                    for f in futures:
                        f.cancel()
                    raise result.exception()

    def validate_local_dataset_storage(self, 
                                       dataset_name: str, 
                                       splits: List[FoundrySplit] = None):
        """ Verifies that the local storage location exists and all expected files are present.

        Args:
            dataset_name (str): name of dataset (equivalrnt to source_id in MDF)
            splits List[FoundrySplit]: Labels of splits to be loaded

        Returns:
            bool: True if exists, else false
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
                if len(os.listdir(path)) <= 1:
                    logger.info("Dataset has already been downloaded and contains all the desired files")
                    return True
                else:
                    logger.debug('Dataset is not complete')
                    return False
        else:
            logger.debug('Dataset is not present')
            return False

    def load_as_dict(self, 
                     dataset_name: str,
                     foundry_schema: FoundrySchema = None, 
                     globus: bool = True, 
                     as_hdf5: bool = False):
        """Load in the data associated with the prescribed dataset

        Tabular Data Type: Data are arranged in a standard data frame
        stored in self.dataframe_file. The contents are read, and

        File Data Type: <<Add desc>>

        For more complicated data structures, users should
        subclass FoundryDataset and override the load_data function

        Args:
            dataset_name (str): name of dataset (equivalrnt to source_id in MDF)
            foundry_schema (FoundrySchema): schema element as obtained from MDF
            splits List[FoundrySplit]: Labels of splits to be loaded
            globus (bool): If True, download using Globus, otherwise https
            as_hdf5 (bool): If True and dataset is in hdf5 format, keep data in hdf5 format

        Returns:
             (dict): a labeled dictionary of tuples
        """

        data = {}

        # Handle splits if they exist. Return as a labeled dictionary of tuples
        try:
            if hasattr(foundry_schema, 'splits'):
                for split in foundry_schema.splits:
                    data[split.label] = self._load_data(foundry_schema=foundry_schema,
                                                        file=split.path, 
                                                        source_id=dataset_name, 
                                                        globus=globus,
                                                        as_hdf5=as_hdf5)
                return data
            else:
                return {"data": self._load_data(foundry_schema=foundry_schema,
                                                source_id=dataset_name, 
                                                globus=globus, 
                                                as_hdf5=as_hdf5)}
        except Exception as e:
            raise Exception(
                "FoundryDataset not loaded!") from e

    def _load_data(self, 
                   foundry_schema: FoundrySchema,
                   file: str ="foundry_dataframe.json", 
                   source_id: str = None, 
                   globus: bool = True, 
                   as_hdf5: bool = False):
        
        # Build the path to access the cached data
        path = os.path.join(self.local_cache_dir, source_id)
        
        if path is None:
            raise ValueError(f"Path to data file is invalid; check that dataset source_id is valid: "
                             f"{source_id or self.mdf['source_id']}")
        
        path_to_file = os.path.join(path, file)

        # Check to see whether file exists at path
        if not os.path.isfile(path_to_file):
            raise FileNotFoundError(f"No file found at expected path: {path_to_file}")

        # Handle Foundry-defined types.
        if foundry_schema.data_type.value == "tabular":
            # TODO: Add hashes and versioning to metadata and checking to the file
            read_fns = [(_read_json, {"lines": False, "path_to_file": path_to_file}),
                        (_read_json, {"lines": True, "path_to_file": path_to_file}),
                        (_read_csv, {"path_to_file": path_to_file}),
                        (_read_excel, {"path_to_file": path_to_file})]

            for fn, params in read_fns:
                try:
                    foundry_schema.dataframe = fn(**params)
                except Exception as e:
                    logger.info(f"Unable to read file with {fn.__name__} with params {params}: {e}")
                if foundry_schema.dataframe is not None:
                    logger.info(f"Succeeded with {fn.__name__} with params {params}")
                    break
            if foundry_schema.dataframe is None:
                logger.fatal(f"Cannot read {path_to_file} as tabular data, failed to load")
                raise ValueError(f"Cannot read tabular data from {path_to_file}")

            return (
                foundry_schema.dataframe[self.get_keys(foundry_schema, "input")],
                foundry_schema.dataframe[self.get_keys(foundry_schema, "target")],
            )

        elif foundry_schema.data_type.value == "hdf5":
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
            if answer.lower() in ["y","yes"]:
                path = os.path.join(self.local_cache_dir, dataset_name)
            else:
                return
        else:
            answer = input(f"This will delete ALL of the data in {self.local_cache_dir} - are you sure you want to continue? (y/n)")
            if answer.lower() in ["y","yes"]:
                path = self.local_cache_dir
            else:
                return
        if os.path.isdir(path):
            shutil.rmtree(path)
