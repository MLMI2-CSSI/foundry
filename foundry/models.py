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

    def __init__(self, **project_dict: Any): # Changed to accept **kwargs for direct dict unpacking
        try:
            super().__init__(**project_dict)
        except ValidationError as e:
            # Removed print statements, rely on caller to handle ValidationError
            # logger.error(f"FoundrySchema validation failed: {e.errors()}") # Optional: log here if desired
            raise e


class FoundryDatacite(DataciteModel):
    """
    A model for the Datacite schema based on the Datacite (dc_model.py) class.
    """
    def __init__(self, **datacite_dict: Any): # Changed to accept **kwargs for direct dict unpacking
        try:
            # The __root__ handling is a workaround for a specific data shape.
            # It's kept, but ideally, the input data should conform to the schema.
            dc_copy = datacite_dict.copy() # Operate on a copy
            if 'identifier' in dc_copy:
                if isinstance(dc_copy['identifier'], dict) and 'identifier' in dc_copy['identifier']:
                    if isinstance(dc_copy['identifier']['identifier'], dict) and '__root__' in dc_copy['identifier']['identifier']:
                        logger.debug("Applying __root__ workaround for identifier in FoundryDatacite")
                        dc_copy['identifier']['identifier'] = dc_copy['identifier']['identifier']['__root__']
            super().__init__(**dc_copy)
        except ValidationError as e:
            # Removed print statements, rely on caller to handle ValidationError
            # logger.error(f"FoundryDatacite validation failed: {e.errors()}") # Optional: log here if desired
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
