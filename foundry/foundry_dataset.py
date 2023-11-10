import json
import logging
import os

from json2table import convert
import pandas as pd
import numpy as np

from foundry.models import FoundrySchema
from pydantic import ValidationError


logger = logging.getLogger(__name__)


class FoundryDataset(FoundrySchema):
    """Representation of an individual dataset.
        Provides access to metadata as well as functions to
        instantiate data into memory in different formats.

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

    def __init__(self, source_id: str, datacite_entry: dict, foundry_schema: FoundrySchema):
        self.source_id = source_id
        self.dc = datacite_entry
        self.foundry_schema = foundry_schema

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
        ...

    def load_data(self, source_id=None, globus=True, as_hdf5=False, splits=[]):
        """Load in the data associated with the prescribed dataset

        Tabular Data Type: Data are arranged in a standard data frame
        stored in self.dataframe_file. The contents are read, and

        File Data Type: <<Add desc>>

        For more complicated data structures, users should
        subclass FoundryDataset and override the load_data function

        Args:
           inputs (list): List of strings for input columns
           targets (list): List of strings for output columns
           source_id (string): Relative path to the source file
           as_hdf5 (bool): If True and dataset is in hdf5 format, keep data in hdf5 format
           splits (list): Labels of splits to be loaded

        Returns:
             (dict): a labeled dictionary of tuples
        """
        data = {}

        # Handle splits if they exist. Return as a labeled dictionary of tuples
        try:
            if self.dataset.splits:
                if not splits:
                    for split in self.dataset.splits:
                        data[split.label] = self._load_data(file=split.path, source_id=source_id, globus=globus,
                                                            as_hdf5=as_hdf5)
                else:
                    for split in self.dataset.splits:
                        if split.label in splits:
                            splits.remove(split.label)
                            data[split.label] = self._load_data(file=split.path, source_id=source_id, globus=globus,
                                                                as_hdf5=as_hdf5)
                    if len(splits) > 0:
                        raise ValueError(f'The split(s) {splits} were not found in the dataset!')
                return data
            else:
                # raise an error if splits are specified but not present in the dataset
                if len(splits) > 0:
                    raise ValueError(f"Splits to load were specified as {splits}, but no splits are present in dataset")
                return {"data": self._load_data(source_id=source_id, globus=globus, as_hdf5=as_hdf5)}
        except Exception as e:
            raise Exception(
                "Metadata not loaded into Foundry object, make sure to call load()") from e

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

            buf = f'{buf}<h3>Dataset</h3>{convert(json.loads(self.dataset.json(exclude={"dataframe"})))}'
        return buf
