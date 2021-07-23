from typing import List, Dict, Optional, Any
from pydantic import BaseModel, AnyHttpUrl
from enum import Enum
import pandas as pd
from json2table import convert
import json

# class FoundryMetric(BaseModel):
#     pass

# class FoundryChallenge(BaseModel):
#     id: int = None
#     metric: FoundryMetric = None
#     datasets: List[FoundryDataset] = []
#     description: str = ""


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
        for i, row in df.drop_duplicates().iterrows():
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


class FoundryKeyClass(BaseModel):
    label: str = ""
    name: str = ""


class FoundryKey(BaseModel):
    key: List[str] = []
    type: str = ""
    filter: Optional[str] = ""
    units: Optional[str] = ""
    description: Optional[str] = ""
    classes: Optional[List[FoundryKeyClass]]


class FoundrySplit(BaseModel):
    type: str = ""
    path: Optional[str] = ""
    label: Optional[str] = ""


class FoundryDataset(BaseModel):
    """Foundry Dataset
    Schema for Foundry Datasets. This includes specifications of inputs, outputs, type, version, and more
    """

    keys: List[FoundryKey] = None
    splits: Optional[List[FoundrySplit]] = None
    data_type: FoundryDatasetType = None
    # version: Optional[str] = ""
    short_name: Optional[str] = ""
    dataframe: Optional[Any] = None
    # links: Optional[FoundryLinks]
    # citations: Optional[List[str]] = []
    task_type: Optional[List[str]] = []
    domain: Optional[List[str]] = []
    n_items: Optional[int] = 0

    class Config:
        arbitrary_types_allowed = True


class FoundryConfig(BaseModel):
    """Foundry Configuration
    Configuration information for Foundry Dataset

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


class FoundryMetadata(BaseModel):
    dc: Optional[Dict] = {}  # pydantic Datacite?
    mdf: Optional[Dict] = {}
    dataset: FoundryDataset = {}
    config: FoundryConfig = FoundryConfig(
        dataframe_file="foundry_dataframe.json",
        metadata_file="foundry_metadata.json",
        local=False,
        local_cache_dir="./data",
    )

    class Config:
        arbitrary_types_allowed = True
