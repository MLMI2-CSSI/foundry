import json
import logging
import os

from json2table import convert
from mdf_forge import Forge
import numpy as np
from pydantic import ValidationError, Extra
from typing import List, Any

from .foundry_cache import FoundryCache
from foundry.models import FoundrySchema, FoundrySplit


logger = logging.getLogger(__name__)


class FoundryDataset():
    """Representation of an individual dataset.
        Provides access to metadata as well as functions to
        instantiate data into memory in different formats.
        
        Args:
            dataset_name (str): name of dataset (equivalent to source_id in MDF)
            splits List[FoundrySplit]: list of splits in the dataset
            globus (bool): if True, use Globus to download the data else try HTTPS
            interval (int): How often to wait before checking Globus transfer status
            parallel_https (int): Number of files to download in parallel if using HTTPS
            verbose (bool): Produce more debug messages to screen

        Desired functions:
            - Get as pandas
            - Get as tensorflow dataset
            - Get as pytorch dataset
            - Get file list
            - Set metadata
            - Attach datafiles
            - Validate against schema
            - Get citation
        """

    def __init__(self, 
                 dataset_name: str, 
                 datacite_entry: dict,
                 transfer_client: Any, 
                 foundry_schema: FoundrySchema, 
                 globus: bool = False,
                 interval: int = 10,
                 parallel_https: int = 4,
                 verbose: bool = False,
                 forge_client: Forge = None):

        self.dataset_name = dataset_name
        self.dc = datacite_entry
        self.transfer_client = transfer_client
        self.foundry_schema = foundry_schema
        self.globus = globus
        self.interval = interval
        self.parallel_https = parallel_https
        self.verbose = verbose
        self._foundry_cache = FoundryCache(forge_client, transfer_client)
 
    def get_as_dict(self, split: str=None):
        """Convert FoundryDatset to a Pandas Dataframe object

        Arguments:
            split (string): Split to create PyTorch Dataset on.
                    **Default:** ``None``

        Returns: (Pandas.Dataframe) Pandas ddataframe of all the data from the specified split

        """
        self.download_if_not_downloaded()
        return self._foundry_cache.load_as_dict(self.dataset_name,
                                                self.foundry_schema,
                                                self.globus)


    def to_pandas(self, split: str=None):
        """Convert FoundryDatset to a Pandas Dataframe object

        Arguments:
            split (string): Split to create PyTorch Dataset on.
                    **Default:** ``None``

        Returns: (Pandas.Dataframe) Pandas ddataframe of all the data from the specified split

        """

        self.download_if_not_downloaded()

    def to_torch(self, split: str = None):
        """Convert Foundry Dataset to a PyTorch Dataset

        Arguments:
            split (string): Split to create PyTorch Dataset on.
                    **Default:** ``None``

        Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split

        """

        self.download_if_not_downloaded()

        from foundry.loaders.torch_wrapper import TorchDataset

        inputs, targets = self._get_inputs_targets(split)
        return TorchDataset(inputs, targets)

    def to_tensorflow(self, split: str = None):
        """Convert Foundry Dataset to a Tensorflow Sequence

        Arguments:
            split (string): Split to create Tensorflow Sequence on.
                    **Default:** ``None``

        Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split

        """
        from foundry.loaders.tf_wrapper import TensorflowSequence

        inputs, targets = self._get_inputs_targets(split)
        return TensorflowSequence(inputs, targets)

    def download_if_not_downloaded(self):
        self._foundry_cache.download_to_cache(self.dataset_name, 
                                              self.foundry_schema.splits, 
                                              self.globus, 
                                              self.interval, 
                                              self.parallel_https, 
                                              self.verbose,
                                              self.transfer_client)

    def get_citation(self) -> str:
        subjects = [subject['subject'] for subject in self.dc['subjects']]
        doi_str = f"doi = {{{self.dc['identifier']['identifier']}}}"
        url_str = f"url = {{https://doi.org/{self.dc['identifier']['identifier']}}}"
        author_str = f"author = {{{' and '.join([creator['creatorName'] for creator in self.dc['creators']])}}}"
        title_str = f"title = {{{self.dc['titles'][0]['title']}}}"
        keywords_str = f"keywords = {{{', '.join(subjects)}}}"
        publisher_str = f"publisher = {{{self.dc['publisher']}}}"
        year_str = f"year = {{{self.dc['publicationYear']}}}"
        bibtex = os.linesep.join([doi_str, url_str,
                                  author_str, title_str,
                                  keywords_str, publisher_str,
                                  year_str])
        bibtex = f"@misc{{https://doi.org/{self.dc['identifier']['identifier']}{os.linesep}{bibtex}}}"
        return bibtex

    def validate_metadata(self, metadata):
        """Validate the JSON message against the FoundryDataset model

        Arguments:
            metadata (dict): Metadata information provided by the user.

        Raises:
            ValidationError: if metadata supplied by user does not meet the specificiation of a
            FoundryDataset object.

        """
        try:
            FoundryDataset(**metadata)
            logger.debug("Metadata validation successful!")
        except ValidationError as e:
            logger.error("Metadata validation failed!")
            for error in e.errors():
                field_name = ".".join([item for item in error['loc'] if isinstance(item, str)])
                error_description = error['msg']
                error_message = f"""There is an issue validating the metadata for the field '{field_name}':
                The error message returned is: '{error_description}'."""
                logger.error(error_message)
            raise e

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

        if self.dataset.data_type.value == "hdf5":
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

        elif self.dataset.data_type.value == "tabular":
            inputs = []
            targets = []

            for index, arr in enumerate([inputs, targets]):
                df = raw[split][index]
                for key in df.keys():
                    arr.append(df[key].values)

            return (inputs, targets)

        else:
            raise NotImplementedError

    def clear_dataset_cache(self):
        """Deletes the cached data for this specific datset"""
        self._foundry_cache.clear_cache(self.dataset_name)

    def _repr_html_(self) -> str:
        """Not sure what this is for or if it is ever called"""

        if not self.dc:
            buf = str(self)
        else:
            title = self.dc['titles'][0]['title']
            authors = [creator['creatorName']
                       for creator in self.dc['creators']]
            authors = '; '.join(authors)
            DOI = "DOI: " + self.dc['identifier']['identifier']

            buf = f'<h2>{title}</h2>{authors}<p>{DOI}</p>'

            buf = f'{buf}<h3>Dataset</h3>{convert(json.loads(self.foundry_schema.json(exclude={"dataframe"})))}'
        return buf
