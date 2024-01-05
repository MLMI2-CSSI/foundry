import logging
import os

from mdf_forge import Forge
from pydantic import ValidationError
from typing import Any

from .foundry_cache import FoundryCache
from foundry.models import FoundrySchema


logger = logging.getLogger(__name__)


class FoundryDataset():
    """Representation of an individual dataset.
        Provides access to metadata as well as functions to
        instantiate data into memory in different formats.

        Args:
            dataset_name (str): name of dataset (equivalent to source_id in MDF)
            splits List[FoundrySplit]: list of splits in the dataset
            use_globus (bool): if True, use Globus to download the data else try HTTPS
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
                 use_globus: bool = False,
                 interval: int = 10,
                 parallel_https: int = 4,
                 verbose: bool = False,
                 forge_client: Forge = None,
                 local_cache_dir: str = None):

        self.dataset_name = dataset_name
        self.dc = datacite_entry
        self.transfer_client = transfer_client
        self.foundry_schema = foundry_schema
        self.use_globus = use_globus
        self.interval = interval
        self.parallel_https = parallel_https
        self.verbose = verbose
        self._foundry_cache = FoundryCache(forge_client, transfer_client, local_cache_dir)

    def get_as_dict(self, split: str = None, as_hdf5: bool = False):
        """Returns the data from the dataset as a dictionary

        Arguments:
            split (string): Split to create dataset on.
                    **Default:** ``None``

        Returns: (dict) Dictionary of all the data from the specified split

        """
        return self._foundry_cache.load_as_dict(split,
                                                self.dataset_name,
                                                self.foundry_schema,
                                                self.use_globus,
                                                self.interval,
                                                self.parallel_https,
                                                self.verbose,
                                                self.transfer_client,
                                                as_hdf5)

    def to_pandas(self, split: str = None):
        """Convert FoundryDatset to a Pandas Dataframe object

        Arguments:
            split (string): Split to create dataset on.
                    **Default:** ``None``

        Returns: (Pandas.Dataframe) Pandas ddataframe of all the data from the specified split

        """
        pass

    def get_as_torch(self, split: str = None):
        """Returns the data from the dataset as a TorchDataset

        Arguments:
            split (string): Split to create PyTorch Dataset on.
                    **Default:** ``None``

        Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split

        """

        return self._foundry_cache.load_as_torch(split,
                                                 self.dataset_name,
                                                 self.foundry_schema,
                                                 self.use_globus,
                                                 self.interval,
                                                 self.parallel_https,
                                                 self.verbose,
                                                 self.transfer_client)

    def get_as_tensorflow(self, split: str = None):
        """Convert Foundry Dataset to a Tensorflow Sequence

        Arguments:
            split (string): Split to create Tensorflow Sequence on.
                    **Default:** ``None``

        Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split

        """
        return self._foundry_cache.load_as_tensorflow(split,
                                                      self.dataset_name,
                                                      self.foundry_schema,
                                                      self.use_globus,
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

    def clear_dataset_cache(self):
        """Deletes the cached data for this specific datset"""
        self._foundry_cache.clear_cache(self.dataset_name)
