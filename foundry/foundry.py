
from pydantic import AnyUrl, ValidationError, BaseModel
from typing import List, Dict, Optional, Any
from collections import namedtuple
from dlhub_sdk import DLHubClient
from mdf_forge import Forge
from mdf_connect_client import MDFConnectClient
import mdf_toolbox
from enum import Enum
import pandas as pd
import requests
import json
import glob
import os

"""
TODO: 
* Merge functionality from dlhub_sdk (remove in dlhub_sdk)
* Split FoundrySources into separate file
* Caching for datasets
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
    #hash: Optional[str] = []
    version: Optional[str] = ""
    short_name: Optional[str] = ""
    #references: Optional[List[str]] = []
    dataframe: Optional[Any] = None
    #sources: Optional[List[AnyUrl]] = []

    class Config:
        arbitrary_types_allowed = True

class FoundryConfig(BaseModel):
    dataframe_file: Optional[str] = "foundry_dataframe.json"
    metadata_file: Optional[str] = "foundry_metadata.json"
    destination_endpoint: Optional[str] = None
    local: Optional[bool] = False
    local_cache_dir = "./data"
    
class FoundryMetadata(BaseModel):
    dc: Optional[Dict] = {} #pydantic Datacite?
    mdf: Optional[Dict] = {}
    dataset: FoundryDataset = {}
    config: FoundryConfig = FoundryConfig(dataframe_file="foundry_dataframe.json",
                                          metadata_file="foundry_metadata.json",
                                          local=False,
                                          local_cache_dir="./data")

    class Config:
        arbitrary_types_allowed = True

class Foundry(FoundryMetadata):
    from_file: Optional[bool]

    __services = ["transfer"]
    __app_name = "Foundry"

    dlhub_client = DLHubClient()
    forge_client = Forge('mdf-test', services=__services)
    transfer_client = mdf_toolbox.login(services=__services, app_name=__app_name)['transfer']
    connect_client = MDFConnectClient(test=True)

    def from_file(self, file=None):
        if file is None: file= self.config.metadata_file
        with open ("./{}".format(file)) as fp:
            obj = json.load(fp)
            return Foundry(**obj)

    def load(self, name, download=True, **kwargs):
        """ 
        Load the contents of a foundry dataset package 
        
        """
        # MDF specific logic
        res = self.forge_client.search('mdf.source_id:{name}'.format(name=name), advanced=True)
        res = res[0]
        res['dataset'] = res['projects']['foundry']
        res['dataset']['type'] = res['dataset']['package_type']
        del(res['projects']['foundry'])

        self = Foundry(**res)

        if download is True: # Add check for package existence
            self.download(interval=kwargs.get('interval', 10))

        return self

    def list(self):
        res = self.forge_client.match_field('mdf.organizations','foundry').search()
        return pd.DataFrame([{"source_id":r['mdf']['source_id'], 
                              "name":r['dc']['titles'][0]['title'],
                              "year":r['dc']['publicationYear']} for r in res])

    def get_packages(self, paths=False):
        pkg_paths = glob.glob(self.config.local_cache_dir+'/*/')
        if paths:
            return [{"path":path, 
                    "package":path.split('/')[-2]} for path in pkg_paths]
        else:
            return [path.split('/')[-2] for path in pkg_paths]
            
    def collect_dataframes(self, inputs=[], outputs=[], packages=None):
        frame_files = glob.glob(self.config.local_cache_dir+'/*/*dataframe*', 
                                recursive=True)

        frames = []
        for frame in frame_files:
            df_tmp = pd.read_json(frame)
            df_tmp['source'] = frame
            frames.append(df_tmp)
        df = pd.concat(frames)

        if inputs and outputs:
            return df[inputs], df[outputs]            
        else:
            return df


    def run(self, name, X, **kwargs):
        # run the model with given data
        return self.dlhub_client.run(name, inputs=X)

    def load_data(self, source_id=None):
        """
        Load in the data associated with the prescribed dataset
        Returns: Tuple of X, y values

        Tabular Data Type: Data are arranged in a standard data frame
        stored in self.dataframe_file. The contents are read, and 

        File Data Type: <<Add desc>>

        For more complicated data structures, users should
        subclass Foundry and override the load_data function 
        """

        if source_id:
            path = os.path.join(self.config.local_cache_dir, source_id)
        else: 
            path = os.path.join(self.config.local_cache_dir, self.mdf['source_id'])
        # Handle Foundry-defined types.
        if self.dataset.type.value == "tabular":
            # If the file is not local, fetch the contents with Globus
            # Check if the contents are local 
            # TODO: Add hashes and versioning to metadata and checking to the file
            # for source in self.dataset.sources:
            #     r = requests.get(source, allow_redirects=True)
            #     open(self.config.dataframe_file, 'wb').write(r.content)

            try:
                self.dataset.dataframe = pd.read_json(os.path.join(path, 
                                                                   self.config.dataframe_file))
            except:
                # Try to read individual lines instead
                self.dataset.dataframe = pd.read_json(os.path.join(path, 
                                                                   self.config.dataframe_file), lines=True)

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

    def publish(self, foundry_metadata, update=False,  **kwargs):
        """
        Submit a data package
        """
        print(kwargs)

        self.connect_client.create_dc_block(title=kwargs['title'],
                   authors=kwargs['authors'],
                   affiliations=kwargs.get('affiliations',[]),
                   subjects = kwargs.get('tags',["machine learning","foundry"]))
        self.connect_client.add_organization("Foundry")
        self.connect_client.set_project_block("foundry", foundry_metadata)
        self.connect_client.add_data_source(kwargs.get('data_sources',[]))

        res = self.connect_client.submit_dataset(update=update)
        return res

        
    def from_file(self, file=None):
        if file is None: file= self.config.metadata_file
        with open ("./{}".format(file)) as fp:
            obj = json.load(fp)
            return Foundry(**obj)

    def to_file(self, file=None):
        if file is None: file= self.config.metadata_file
        with open ("./{}".format(file)) as fp:
            obj = json.dump(self.json(exclude={"dlhub_client","forge_client"}), fp)

    def configure(self, **kwargs):
        self.config = FoundryConfig(**kwargs)
        return self

    def download(self, **kwargs):
        #Check if the dir already exists
        if os.path.isdir(os.path.join(self.config.local_cache_dir, self.mdf['source_id'])):
            return self

        res = self.forge_client.search('mdf.source_id:{name}'.format(name=self.mdf['source_id']), advanced=True)
        self.forge_client.globus_download(res, dest=self.config.local_cache_dir, 
                                          dest_ep=self.config.destination_endpoint, 
                                          interval=kwargs.get('interval',20),
                                          download_datasets=True)
        return self
