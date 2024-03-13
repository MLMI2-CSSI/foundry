import copy
from enum import Enum
import json
from json2table import convert
import logging
import pandas as pd
from pydantic import BaseModel, Extra, ValidationError
from typing import Optional, Any

from .dc_model import Dc1 as DataciteModel
from .project_model import Foundry as FoundryModel

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


# END Classes for Foundry Data Package Specification


class FoundryDatasetType(Enum):
    """Foundry Dataset Types
    Enumeration of the possible Foundry dataset types
    """

    tabular = "tabular"
    files = "files"
    hdf5 = "hdf5"
    other = "other"


# overridden by project_model.py
# class FoundryKeyClass(BaseModel):
#     label: StrictStr = Field(..., description="The label that exists in the data")
#     name: StrictStr = Field(..., description="The name the label maps onto.")
# 
# 
# class FoundryKey(BaseModel):
#     key: List[StrictStr] = Field(..., description="Column or header name for tabular data, key/path for HDF5 data")
#     type: StrictStr = Field(..., description="Whether input or target")
#     classes: Optional[List[FoundryKeyClass]]
#     description: Optional[StrictStr]
#     filter: Optional[StrictStr]
#     units: Optional[StrictStr]
# 
# 
# class FoundrySplit(BaseModel):
#     type: StrictStr = Field(..., description="The kind of partition of the dataset (train, test, validation, etc)")
#     path: Optional[StrictStr]
#     label: Optional[StrictStr]
#
#
# replacing with definition from project_model.py
# class FoundrySchema(BaseModel):
#    """Foundry Dataset
#    Schema for Foundry Datasets. This includes specifications of inputs, outputs, type, version, and more
#    """
#    data_type: FoundryDatasetType = Field(..., description="The kind of data in the dataset, e.g. tabular, json, hdf5")
#    domain: List[StrictStr] = Field(..., description="The domain of applicability. e.g., materials science, chemistry, machine vision")
#    keys: List[FoundryKey] = Field(..., description="Keys describing how to load the data")
#    dataframe: Optional[Any]
#    n_items: Optional[StrictInt]
#    short_name: Optional[StrictStr]
#    splits: Optional[List[FoundrySplit]]
#    task_type: Optional[List[StrictStr]]
#    schema_url = 'https://raw.githubusercontent.com/materials-data-facility/data-schemas/master/schemas/projects.json'
# 
#    class Config:
#        arbitrary_types_allowed = True
#        extra = Extra.allow


class FoundrySchema(FoundryModel):
    def __init__(self, project_dict):
        try:
            super(FoundrySchema, self).__init__(**project_dict)
            print("FoundrySchema validation successful.")
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
    def __init__(self, datacite_dict):
        try:
            # modify the datacite_entry to match the expected format
            dc = copy.deepcopy(datacite_dict)

            if 'identifier' in dc.keys():
                if 'identifier' in dc['identifier'].keys():
                    dc['identifier']['identifier'] = {'__root__': datacite_dict['identifier']['identifier']}
            super(FoundryDatacite, self).__init__(**dc)
            print("Datacite validation successful.")
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


# class FoundryDataset(BaseModel):
#     """Foundry Dataset
#     Schema for Foundry Datasets. This includes specifications of inputs, outputs, type, version, and more
#     """
# 
#     keys: List[FoundryKey] = None
#     splits: Optional[List[FoundrySplit]] = None
#     data_type: FoundryDatasetType = None
#     # version: Optional[str] = ""
#     short_name: Optional[str] = ""
#     dataframe: Optional[Any] = None
#     # links: Optional[FoundryLinks]
#     # citations: Optional[List[str]] = []
#     task_type: Optional[List[str]] = []
#     domain: Optional[List[str]] = []
#     n_items: Optional[int] = 0
# 
#     class Config:
#         arbitrary_types_allowed = True


class FoundryBase(BaseModel, extra=Extra.allow):
    """Configuration information for Foundry instance

    Args:
        dataframe_file (str): Filename to read dataframe contents from
        metadata_file (str): Filename to read metadata contents from defaults to reading for MDF Discover
        destination_endpoint (str): Globus endpoint ID to transfer data to (defaults to local GCP installation)
        local_cache_dir (str): Path to local Foundry package cache
    """

    dataframe_file: Optional[str] = "foundry_dataframe.json"
    data_file: Optional[str] = "foundry.hdf5"
    metadata_file: Optional[str] = "foundry_metadata.json"
    destination_endpoint: Optional[str] = None
    local: Optional[bool] = False
    local_cache_dir = "./data"
    metadata_key: Optional[str] = "foundry"
    organization: Optional[str] = "foundry"

    def _repr_html_(self):
        return convert(json.loads(self.json()))


# class FoundryDataset(BaseModel, extra=Extra.allow):
#     dc: Dict = {}  # pydantic Datacite?
#     mdf: Dict = {}
#     dataset: FoundryDataset = {}
