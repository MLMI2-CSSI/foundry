import copy
from enum import Enum
import json
from json2table import convert
import logging
import pandas as pd
from pydantic import BaseModel, Extra, ValidationError
from typing import Optional, Any

from .jsonschema_models.dc_model import Dc1 as DataciteModel
from .jsonschema_models.project_model import Foundry as FoundryModel

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)


# Classes for Foundry Data Package Specification
class FoundrySpecificationDataset(BaseModel):
    """Pydantic base class for datasets within the Foundry data package specification"""

    name: Optional[str]
    provider: Optional[str] = "MDF"
    version: Optional[str]


class FoundrySpecification(BaseModel):
    """Pydantic base class for interacting with the Foundry data package specification
    The specification provides a way to group datasets and manage versions
    """

    name: str = ""
    version: str = ""
    description: str = ""
    private: bool = False
    dependencies: Any  # List[FoundrySpecificationDataset]

    def add_dependency(self, name, version):
        self.dependencies[name] = version

    def remove_duplicate_dependencies(self):

        deps = [{"name": key, "version": self.dependencies[key]}
                for key in self.dependencies]
        df = pd.DataFrame.from_records(deps)
        self.clear_dependencies()
        for _, row in df.drop_duplicates().iterrows():
            self.add_dependency(name=row["name"], version=row["version"])

    def clear_dependencies(self):
        self.dependencies = {}

    def _repr_html_(self):
        buf = f'<h3>Data Requirements - {self.name}</h3>'
        buf = buf + convert(json.loads(self.json()))
        return buf


class FoundryDatasetType(Enum):
    """Foundry Dataset Types
    Enumeration of the possible Foundry dataset types
    """

    tabular = "tabular"
    files = "files"
    hdf5 = "hdf5"
    other = "other"


class FoundrySchema(FoundryModel):
    """
    A model for the Foundry schema based on the FoundryModel (project_model.py) class. The FoundryModel
    class is an auto-generated pydantic version of the json schema; this class extends
    the FoundryModel class to include additional functionality necessary for Foundry.

    Args:
        project_dict (dict): A dictionary containing the project data.

    Raises:
        ValidationError: If there is an issue validating the project data.
    """

    def __init__(self, project_dict):
        try:
            super(FoundrySchema, self).__init__(**project_dict)
        except ValidationError as e:
            print("FoundrySchema validation failed!")
            for error in e.errors():
                field_name = ".".join([item for item in error['loc'] if isinstance(item, str)])
                error_description = error['msg']
                error_message = f"""There is an issue validating the entry for the field '{field_name}':
                The error message returned is: '{error_description}'.
                The description for this field is: '{FoundryModel.schema()['properties'][field_name]['description']}'"""
                print(error_message)
            raise e


class FoundryDatacite(DataciteModel):
    """
    A model for the Datacite schema based on the Datacite (dc_model.py) class. The FoundryModel
    class is an auto-generated pydantic version of the json schema; this class extends
    the DataciteModel class to include additional functionality necessary for Foundry.

    Args:
        datacite_dict (dict): A dictionary containing the datacite data.

    Raises:
        ValidationError: If there is an issue validating the datacite data.
    """
    def __init__(self, datacite_dict, extra=Extra.allow):
        try:
            # modify the datacite_entry to match the expected format
            dc_dict = copy.deepcopy(datacite_dict)
            if 'identifier' in dc_dict.keys():
                if 'identifier' in dc_dict['identifier'].keys():
                    dc_dict['identifier']['identifier'] = {'__root__': datacite_dict['identifier']['identifier']}
            super(FoundryDatacite, self).__init__(**dc_dict)
        except ValidationError as e:
            print("Datacite validation failed!")
            for error in e.errors():
                # field_name = ".".join([item for item in error['loc'] if isinstance(item, str)])
                field_name = error['loc'][0]
                error_description = error['msg']
                error_message = f"""There is an issue validating the entry for the field '{field_name}':
                The error message returned is: '{error_description}'.
                The description for this field is: '{FoundryDatacite.schema()['properties'][field_name]['description']}'"""
                print(error_message)
            raise e


class FoundryBase(BaseModel, extra=Extra.allow):
    """
    Configuration information for Foundry instance

    Args:
        dataframe_file (str, optional): Filename to read dataframe contents from (default is "foundry_dataframe.json")
        data_file (str, optional): Filename to read data contents from (default is "foundry.hdf5")
        metadata_file (str, optional): Filename to read metadata contents from (default is "foundry_metadata.json")
        destination_endpoint (str, optional): Globus endpoint ID to transfer data to (default is None)
        local (bool, optional): Flag indicating whether to use local cache (default is False)
        local_cache_dir (str, optional): Path to local Foundry package cache (default is "./data")
        metadata_key (str, optional): Key for metadata (default is "foundry")
        organization (str, optional): Organization name (default is "foundry")
    """

    dataframe_file: Optional[str] = "foundry_dataframe.json"
    data_file: Optional[str] = "foundry.hdf5"
    metadata_file: Optional[str] = "foundry_metadata.json"
    destination_endpoint: Optional[str] = None
    local: Optional[bool] = False
    local_cache_dir = "./data"
    metadata_key: Optional[str] = "foundry"
    organization: Optional[str] = "Foundry"

    def _repr_html_(self):
        return convert(json.loads(self.json()))
