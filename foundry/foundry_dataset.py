import logging
import os

from pydantic import ValidationError

from .foundry_cache import FoundryCache
from .models import FoundrySchema, FoundryDatacite


logger = logging.getLogger(__name__)


class FoundryDataset():
    """Representation of an individual dataset.
        Provides access to metadata as well as functions to
        instantiate data into memory in different formats.

        Args:
            dataset_name (str): Name of the dataset (equivalent to source_id in MDF)
            datacite_entry (FoundryDatacite): Datacite entry for the dataset
            foundry_schema (FoundrySchema): Schema for the dataset
            foundry_cache (FoundryCache): Cache for the dataset

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
                 datacite_entry: FoundryDatacite,
                 foundry_schema: FoundrySchema,
                 foundry_cache: FoundryCache = None):

        self.dataset_name = dataset_name
        try:
            self.dc = FoundryDatacite(datacite_entry)
            self.foundry_schema = FoundrySchema(foundry_schema)
        except Exception as e:
            raise Exception('there was a problem creating the dataset: ', e)
        self._foundry_cache = foundry_cache

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
                                                as_hdf5)

    def get_as_torch(self, split: str = None):
        """Returns the data from the dataset as a TorchDataset

        Arguments:
            split (string): Split to create PyTorch Dataset on.
                    **Default:** ``None``

        Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split

        """

        return self._foundry_cache.load_as_torch(split,
                                                 self.dataset_name,
                                                 self.foundry_schema)

    def get_as_tensorflow(self, split: str = None):
        """Convert Foundry Dataset to a Tensorflow Sequence

        Arguments:
            split (string): Split to create Tensorflow Sequence on.
                    **Default:** ``None``

        Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split

        """
        return self._foundry_cache.load_as_tensorflow(split,
                                                      self.dataset_name,
                                                      self.foundry_schema)

    def get_citation(self) -> str:
        subjects = [subject.subject for subject in self.dc.subjects]
        doi_str = f"doi = {{{self.dc.identifier.identifier.__root__}}}"
        url_str = f"url = {{https://doi.org/{self.dc.identifier.identifier.__root__}}}"
        author_str = f"author = {{{' and '.join([creator['creatorName'] for creator in self.dc.creators])}}}"
        title_str = f"title = {{{self.dc.titles[0].title}}}"
        keywords_str = f"keywords = {{{', '.join(subjects)}}}"
        publisher_str = f"publisher = {{{self.dc.publisher}}}"
        year_str = f"year = {{{self.dc.publicationYear.__root__}}}"
        bibtex = os.linesep.join([doi_str, url_str,
                                  author_str, title_str,
                                  keywords_str, publisher_str,
                                  year_str])
        bibtex = f"@misc{{https://doi.org/{self.dc.identifier.identifier.__root__}{os.linesep}{bibtex}}}"
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
