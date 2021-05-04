from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from enum import Enum
import pandas as pd

# class FoundryMetric(BaseModel):
#     pass

# class FoundryChallenge(BaseModel):
#     id: int = None
#     metric: FoundryMetric = None
#     datasets: List[FoundryDataset] = []
#     description: str = ""


### Classes for Foundry Data Package Specification
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
    dependencies: List[FoundrySpecificationDataset]

    def add_dependency(self, name, version, provider="MDF"):
        ds = FoundrySpecificationDataset(name=name, provider=provider, version=version)
        self.dependencies.append(ds)

    def remove_duplicate_dependencies(self):
        df = pd.DataFrame(self.dict()["dependencies"])

        self.clear_dependencies()
        for i, row in df.drop_duplicates().iterrows():
            self.add_dependency(name=row["name"], version=row["version"])

    def clear_dependencies(self):
        self.dependencies = []


### END Classes for Foundry Data Package Specification


class FoundryDatasetType(Enum):
    """Foundry Dataset Types
    Enumeration of the possible Foundry dataset types
    """

    tabular = "tabular"
    files = "files"
    hdf5 = "hdf5"
    other = "other"


class FoundryDataset(BaseModel):
    """Foundry Dataset
    Schema for Foundry Datasets. This includes specifications of inputs, outputs, type, version, and more
    """

    inputs: List = []
    outputs: List = []
    input_descriptions: Optional[List] = []
    output_descriptions: Optional[List] = []
    type: FoundryDatasetType = None
    # hash: Optional[str] = []
    version: Optional[str] = ""
    short_name: Optional[str] = ""
    # references: Optional[List[str]] = []
    dataframe: Optional[Any] = None
    # sources: Optional[List[AnyUrl]] = []

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
