
from pydantic import AnyUrl, ValidationError, BaseModel
from typing import List, Dict, Optional, Any
from collections import namedtuple
from dlhub_sdk import DLHubClient
from mdf_forge import Forge
import mdf_toolbox
from enum import Enum
import pandas as pd
import requests
import json

"""
TODO: 
* Merge functionality from dlhub_sdk (remove in dlhub_sdk)
* Split FoundrySources into separate file
* Caching for datasets
* Support for loading metadata from Search
* List available datasets
* Add arg to describe dataset to accept short_name
* Push and pull functionality for datasets
"""

# class FoundryMetric(BaseModel):
#     pass

# class FoundryChallenge(BaseModel):
#     id: int = None
#     metric: FoundryMetric = None
#     datasets: List[FoundryDataset] = []
#     description: str = ""


class FoundryDatasetType(Enum):
    tabular="tabular"
    files="files"
    other="other"
        
class FoundryDataset(BaseModel):
    inputs: List = []
    outputs: List = []
    input_descriptions: Optional[List] = []
    output_descriptions: Optional[List] = []
    type: FoundryDatasetType = None
    hash: Optional[str] = []
    version: Optional[str] = ""
    references: Optional[List[str]] = []
    dataframe: Optional[Any] = None
    sources: Optional[List[AnyUrl]] = []

    class Config:
        arbitrary_types_allowed = True

class FoundryConfig(BaseModel):
    dataframe_file: Optional[str] = "" 
    metadata_file: Optional[str] = ""
    local: Optional[bool]
    local_cache_dir = ""
    
class FoundryMetadata(BaseModel):
    dc: Optional[Dict] = {} #pydantic Datacite?
    dataset: FoundryDataset = {}
    config: FoundryConfig = FoundryConfig(dataframe_file="foundry_dataframe.json",
                                          metadata_file="foundry_metadata.json",
                                          local=True,
                                          local_cache_dir="~/.foundry")

    class Config:
        arbitrary_types_allowed = True

class Foundry(FoundryMetadata):
    from_file: Optional[bool]

    __services = ["transfer"]
    __app_name = "Foundry"

    dlhub_client = DLHubClient()
    forge_client = Forge('mdf-test', services=__services)
    transfer_client = mdf_toolbox.login(services=__services, app_name=__app_name)['transfer']

    def from_file(self, file=None):
        if file is None: file= self.config.metadata_file
        with open ("./{}".format(file)) as fp:
            obj = json.load(fp)
            return Foundry(**obj)

    def load_dataset(self, name, *args):
        """ 
        Load the contents of a foundry.json file 
        
        """
        # Given the name, find the associated dataset on MDF, 
        # fetch the contents and load the metadata from foundry_meta.json
        raise NotImplementedError

    def run(self, name, X, **kwargs):
        # run the model with given data
        return self.dlhub_client.run(name, inputs=X)

    def load_data(self):
        """
        Load in the data associated with the prescribed dataset
        Returns: Tuple of X, y values

        Tabular Data Type: Data are arranged in a standard data frame
        stored in self.dataframe_file. The contents are read, and 

        File Data Type: <<Add desc>>

        For more complicated data structures, users should
        subclass Foundry and override the load_data function 
        """
        
        # Handle Foundry-defined types.
        if self.dataset.type.value == "tabular":
            # If the file is not local, fetch the contents with Globus
            # Check if the contents are local 
            # TODO: Add hashes and versioning to metadata and checking to the file
            for source in self.dataset.sources:
                r = requests.get(source, allow_redirects=True)
                open(self.config.dataframe_file, 'wb').write(r.content)
            self.dataset.dataframe = pd.read_json('./'+self.config.dataframe_file)
            return self.dataset.dataframe[self.dataset.inputs], self.dataset.dataframe[self.dataset.outputs]
        elif self.dataset.type.value == "file":
            self.dataset.dataframe = pd.read_json('./'+self.config.dataframe_file)
            #self.dereference_columns()
            return self.dataset.dataframe[self.dataset.inputs], self.dataset.dataframe[self.dataset.outputs]
        else:
            raise NotImplementedError

    def dereference_columns(self, reference_char="*"):
        for key in self.dataframe.keys():
            if key[0] == reference_char:
                self.dataframe[key] = self.dataframe[key].map(lambda x: np.load(x))
        return self.dataframe

    def describe(self):
        print("DC:{}".format(self.dc))
        print("Dataset:{}".format(self.dataset.json(exclude={"dataframe"})))

    def submit_dataset(self, args):
        """
        Submit a dataset back
        """

        raise NotImplementedError
        
    def from_file(self, file=None):
        if file is None: file= self.config.metadata_file
        with open ("./{}".format(file)) as fp:
            obj = json.load(fp)
            return Foundry(**obj)

    def to_file(self, file=None):
        if file is None: file= self.config.metadata_file
        with open ("./{}".format(file)) as fp:
            obj = json.dump(self.json(exclude={"dlhub_client","forge_client"}), fp)

    @staticmethod
    def get_data(scheme, host, path):
        """
        Arrange data files on the local system to allow load_data to be invoked
        
        For more complicated data structures, users should
        subclass Foundry and override the load_data function 
        """
        from keras.utils import get_file

        if scheme.lower() == "http" or scheme.lower() == "https":
            origin="{}://{}{}".format(scheme, host, path)
            return get_file("{}".format(path.split('/')[-1]), 
            origin=origin,
            cache_subdir="boston",
            cache_dir="~/.foundry")

