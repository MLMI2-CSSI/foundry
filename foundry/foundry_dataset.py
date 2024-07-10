import json
import logging
import os
import html

from pydantic import ValidationError, BaseModel, Field
from typing import Optional, Dict, Any, List

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
                 cache: FoundryCache = None):

        self.dataset_name = dataset_name
        try:
            self.dc = FoundryDatacite(datacite_entry)
            self.foundry_schema = FoundrySchema(foundry_schema)
        except Exception as e:
            raise Exception('there was a problem creating the dataset: ', e)
        self.cache = cache

    def load(self, split: str = None, as_hdf5: bool = False):
        """Returns the data from the dataset as a dictionary

        Arguments:
            split (string): Split to create dataset on.
                    **Default:** ``None``

        Returns: (dict) Dictionary of all the data from the specified split

        """
        return self.cache.load_as_dict(split,
                                                self.dataset_name,
                                                self.foundry_schema,
                                                as_hdf5)

    def _repr_html_(self):
            html_string = f"""
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                <h3 style="color: #333;">{html.escape(self.dataset_name)}</h3>
                <p><strong>Title:</strong> {html.escape(self.dc.titles[0].title)}</p>
                <p><strong>DOI:</strong> {self.dc.identifier.identifier.__root__}</p>
                <p><strong>Publication Year:</strong> {self.dc.publicationYear.__root__}</p>
                <p><strong>Publisher:</strong> {html.escape(self.dc.publisher)}</p>
                <p><strong>Resource Type:</strong> {self.dc.resourceType.resourceType}</p>
                <p><strong>Authors:</strong></p>
                <ul>
                    {self._format_creators()}
                </ul>
                <p><strong>Tags:</strong> {self._format_subjects()}</p>
                <details>
                    <summary><strong>Description</strong></summary>
                    <p>{html.escape(self.dc.descriptions[0].description if self.dc.descriptions else 'No description available.')}</p>
                </details>
            </div>
            """
            return html_string

    def _format_creators(self):
        creators_list = []
        for creator in self.dc.creators:
            affiliations = creator.get('affiliations', [])
            if affiliations:
                affiliations_str = ', '.join(html.escape(aff) for aff in affiliations)
                creators_list.append(f"{html.escape(creator['creatorName'])} ({affiliations_str})")
            else:
                creators_list.append(f"{html.escape(creator['creatorName'])}")
        return '; '.join(creators_list)
    
    def _format_subjects(self):
            return ', '.join([html.escape(subject.subject) for subject in self.dc.subjects]) if self.dc.subjects else 'No subjects available'
    
    def get_as_torch(self, split: str = None):
        """Returns the data from the dataset as a TorchDataset

        Arguments:
            split (string): Split to create PyTorch Dataset on.
                    **Default:** ``None``

        Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split

        """

        return self.cache.load_as_torch(split,
                                                 self.dataset_name,
                                                 self.foundry_schema)

    def get_as_tensorflow(self, split: str = None):
        """Convert Foundry Dataset to a Tensorflow Sequence

        Arguments:
            split (string): Split to create Tensorflow Sequence on.
                    **Default:** ``None``

        Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split

        """
        return self.cache.load_as_tensorflow(split,
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

    def add_data(self, local_data_path: str = None, globus_data_source: str = None):
        """Add data to the dataset. User must provide the location of the data as
        either a `globus_data_source` or `local_data_path`.

        Arguments:
                local_data_path (str): Local path to the dataset used to publish to Foundry via HTTPS. Creates an HTTPS PUT
                request to upload the data specified to a Globus endpoint (default is NCSA endpoint) before it is
                transferred to MDF. If None, the user must specify a 'globus_data_source' URL to the location of the
                data on their own Globus endpoint. User must choose either `globus_data_source` or `local_data_path` to
                publish their data.
            globus_data_source (str): Url path for a data folder on a Globus endpoint; url can be obtained through
                the Globus Web UI or SDK. If None, the user must specify an 'local_data_path' pointing to the location
                of the data on their local machine. User must choose either `globus_data_source` or `local_data_path` to
                publish their data.

        """
        if local_data_path is None and globus_data_source is None:
            raise ValueError("User must provide either a path to the data on their local machine or a URL to the data "
                             "on their Globus endpoint.")
        if local_data_path is None:
            self._globus_data_source = globus_data_source
            if hasattr(self, '_local_data_path'):
                delattr(self, '_local_data_path')
        if globus_data_source is None:
            if os.path.isdir(local_data_path) or os.path.isfile(local_data_path):
                self._local_data_path = local_data_path
                if hasattr(self, '_globus_data_source'):
                    delattr(self, '_globus_data_source')
            else:
                raise ValueError("The path provided does not exist or is not a file or directory.")

    def clear_dataset_cache(self):
        """Deletes the cached data for this specific datset"""
        self.cache.clear_cache(self.dataset_name)

    def clean_dc_dict(self):
        """Clean the Datacite dictionary of None values"""
        return self.delete_none(json.loads(self.dc.json()))

    def delete_none(self, _dict):
        """Delete None values recursively from all of the dictionaries"""
        for key, value in list(_dict.items()):
            if isinstance(value, dict):
                self.delete_none(value)
            elif value is None:
                del _dict[key]
            elif isinstance(value, list):
                for v_i in value:
                    if isinstance(v_i, dict):
                        self.delete_none(v_i)

        return _dict
