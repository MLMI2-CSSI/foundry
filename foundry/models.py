from enum import Enum
import json
from json2table import convert
import logging
import pandas as pd
from pydantic import BaseModel, Field, Extra, ValidationError
from typing import Optional, Any, Dict

from .jsonschema_models.dc_model import Dc1 as DataciteModel
from .jsonschema_models.project_model import Foundry as FoundryModel

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)


# Classes for Foundry Data Package Specification
class FoundrySpecificationDataset(BaseModel):
    """Pydantic base class for datasets within the Foundry data package specification"""

    name: Optional[str] = None
    provider: Optional[str] = Field(default="MDF")
    version: Optional[str] = None


class FoundrySpecification(BaseModel):
    """Pydantic base class for interacting with the Foundry data package specification
    The specification provides a way to group datasets and manage versions
    """

    name: str = Field(default="")
    version: str = Field(default="")
    description: str = Field(default="")
    private: bool = Field(default=False)
    dependencies: Dict[str, str] = Field(default_factory=dict)

    def add_dependency(self, name: str, version: str):
        self.dependencies[name] = version

    def remove_duplicate_dependencies(self):
        deps = [{"name": key, "version": self.dependencies[key]}
                for key in self.dependencies]
        df = pd.DataFrame.from_records(deps)
        self.clear_dependencies()
        for _, row in df.drop_duplicates().iterrows():
            self.add_dependency(name=row["name"], version=row["version"])

    def clear_dependencies(self):
        self.dependencies.clear()

    def model_dump(self):
        return json.loads(self.model_dump_json())

    def _repr_html_(self):
        buf = f'<h3>Data Requirements - {self.name}</h3>'
        buf = buf + convert(self.model_dump())
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
    A model for the Foundry schema based on the FoundryModel (project_model.py) class.
    """

    def __init__(self, project_dict: Dict[str, Any]):
        try:
            super().__init__(**project_dict)
        except ValidationError as e:
            print("FoundrySchema validation failed!")
            for error in e.errors():
                field_name = ".".join([str(item) for item in error['loc']])
                error_description = error['msg']
                error_message = f"""There is an issue validating the entry for the field '{field_name}':
                The error message returned is: '{error_description}'.
                The description for this field is: '{FoundryModel.model_json_schema()['properties'][field_name]['description']}'"""
                print(error_message)
            raise e


class FoundryDatacite(DataciteModel):
    """
    A model for the Datacite schema based on the Datacite (dc_model.py) class.
    """
    def __init__(self, datacite_dict: Dict[str, Any], **kwargs):
        try:
            dc_dict = datacite_dict.copy()
            if 'identifier' in dc_dict:
                if isinstance(dc_dict['identifier'], dict) and 'identifier' in dc_dict['identifier']:
                    if isinstance(dc_dict['identifier']['identifier'], dict) and '__root__' in dc_dict['identifier']['identifier']:
                        dc_dict['identifier']['identifier'] = dc_dict['identifier']['identifier']['__root__']
            super().__init__(**dc_dict, **kwargs)
        except ValidationError as e:
            print("Datacite validation failed!")
            for error in e.errors():
                field_name = ".".join(str(loc) for loc in error["loc"])
                error_description = error['msg']
                error_message = f"""There is an issue validating the entry for the field '{field_name}':
                The error message returned is: '{error_description}'.
                The description is: '{self.model_json_schema()['properties'].get(field_name, {}).get('description', 'No description available')}'"""
                print(error_message)
            raise e


class FoundryBase(BaseModel):
    """
    Configuration information for Foundry instance
    """

    dataframe_file: Optional[str] = Field(default="foundry_dataframe.json")
    data_file: Optional[str] = Field(default="foundry.hdf5")
    metadata_file: Optional[str] = Field(default="foundry_metadata.json")
    destination_endpoint: Optional[str] = None
    local: Optional[bool] = Field(default=False)
    local_cache_dir: str = Field(default="./data")
    metadata_key: Optional[str] = Field(default="foundry")
    organization: Optional[str] = Field(default="Foundry")

    class Config:
        extra = Extra.allow

    def model_dump(self):
        return json.loads(self.model_dump_json())

    def _repr_html_(self):
        return convert(self.model_dump())
