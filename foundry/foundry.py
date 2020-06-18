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
import glob
import h5py
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


class Foundry(FoundryMetadata):
    """Foundry Client Base Class
    TODO:
    -------
    Add Docstring

    """

    # transfer_client: Any
    dlhub_client: Any
    forge_client: Any
    # connect_client: #Add this back in later, not necessary for current functionality

    def __init__(
        self, no_browser=False, no_local_server=False, search_index="mdf-test", **data
    ):
        super().__init__(**data)
        auths = mdf_toolbox.login(
            services=[
                "data_mdf",
                "search",
                "petrel",
                "transfer",
                "dlhub",
                "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all",
            ],
            app_name="Foundry",
            make_clients=True,
            no_browser=no_browser,
            no_local_server=no_local_server,
        )

        self.forge_client = Forge(
            index=search_index,
            services=None,
            search_client=auths["search"],
            transfer_client=auths["transfer"],
            data_mdf_authorizer=auths["data_mdf"],
            petrel_authorizer=auths["petrel"],
        )

        self.dlhub_client = DLHubClient(
            dlh_authorizer=auths["dlhub"],
            search_client=auths["search"],
            fx_authorizer=auths[
                "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all"
            ],
            force_login=False,
        )

    def load(self, name, download=True, globus=True, **kwargs):
        """Load the metadata for a Foundry dataset into the client

        Args:
            name (str): Name of the foundry dataset
            download (bool): If True, download the data associated with the package (default is True)
    
        Keyword Args:
            interval (int): How often to poll Globus to check if transfers are complete

        Returns
        -------
            self
        """
        # MDF specific logic
        res = self.forge_client.match_field(
            "mdf.organizations", "foundry"
        ).match_resource_types("dataset")
        res = res.match_field("mdf.source_id", name).search()

        res = res[0]
        res["dataset"] = res["projects"]["foundry"]
        res["dataset"]["type"] = res["dataset"]["package_type"]
        del res["projects"]["foundry"]

        self = Foundry(**res)

        if download is True:  # Add check for package existence
            self.download(interval=kwargs.get("interval", 10), globus=globus)

        return self

    def list(self):
        """List available Foundry data packages

        Returns
        -------
            (pandas.DataFrame): DataFrame with summary list of Foundry data packages including name, title, and publication year
        """
        res = (
            self.forge_client.match_field("mdf.organizations", "foundry")
            .match_resource_types("dataset")
            .search()
        )

        return pd.DataFrame(
            [
                {
                    "source_id": r["mdf"]["source_id"],
                    "name": r["dc"]["titles"][0]["title"],
                    "year": r["dc"].get("publicationYear", None),
                }
                for r in res
            ]
        )

    def get_packages(self, paths=False):
        """Get available local data packages

        Args:
           paths (bool): If True return paths in addition to package, if False return package name only

        Returns
        -------
            (list): List describing local Foundry packages
        """
        pkg_paths = glob.glob(self.config.local_cache_dir + "/*/")
        if paths:
            return [
                {"path": path, "package": path.split("/")[-2]} for path in pkg_paths
            ]
        else:
            return [path.split("/")[-2] for path in pkg_paths]

    def collect_dataframes(self, inputs=[], outputs=[], packages=None):
        """Collect dataframes of local data packages
        Args:
           inputs (list): List of strings for input columns
           outputs (list): List of strings for output columns

        Returns
        -------
            (pandas.DataFrame): Collected dataframe with specified inputs and outputs
        """
        frame_files = glob.glob(
            self.config.local_cache_dir + "/*/*dataframe*", recursive=True
        )

        frames = []
        for frame in frame_files:
            df_tmp = pd.read_json(frame)
            df_tmp["source"] = frame
            frames.append(df_tmp)
        df = pd.concat(frames)

        if inputs and outputs:
            return df[inputs], df[outputs]
        else:
            return df

    def run(self, name, inputs, **kwargs):
        """Run a model on data

        Args:
           name (str): DLHub model name
           inputs: Data to send to DLHub as inputs (should be JSON serializable)

        Returns
        -------
             Returns results after invocation via the DLHub service

        TODO:
        -------
        - Pass **kwargs through to DLHub client and document kwargs
        """
        return self.dlhub_client.run(name, inputs=inputs)

    def load_data(self, source_id=None, globus=True):
        """Load in the data associated with the prescribed dataset

        Tabular Data Type: Data are arranged in a standard data frame
        stored in self.dataframe_file. The contents are read, and 

        File Data Type: <<Add desc>>

        For more complicated data structures, users should
        subclass Foundry and override the load_data function 

        Args:
           inputs (list): List of strings for input columns
           outputs (list): List of strings for output columns

        Returns
        -------
             (tuple): Tuple of X, y values
        """

        if source_id:
            path = os.path.join(self.config.local_cache_dir, source_id)
        else:
            path = os.path.join(self.config.local_cache_dir, self.mdf["source_id"])
        # Handle Foundry-defined types.
        if self.dataset.type.value == "tabular":
            # If the file is not local, fetch the contents with Globus
            # Check if the contents are local
            # TODO: Add hashes and versioning to metadata and checking to the file
            try:
                self.dataset.dataframe = pd.read_json(
                    os.path.join(path, self.config.dataframe_file)
                )
            except:
                # Try to read individual lines instead
                self.dataset.dataframe = pd.read_json(
                    os.path.join(path, self.config.dataframe_file), lines=True
                )

            return (
                self.dataset.dataframe[self.dataset.inputs],
                self.dataset.dataframe[self.dataset.outputs],
            )
        elif self.dataset.type.value == "hdf5":
            f = h5py.File(os.path.join(path, self.config.data_file), "r")
            inputs = [f[i[0:]] for i in self.dataset.inputs]
            outputs = [f[i[0:]] for i in self.dataset.outputs]
            return (inputs, outputs)
        else:
            raise NotImplementedError

    def describe(self):
        print("DC:{}".format(self.dc))
        print("Dataset:{}".format(self.dataset.json(exclude={"dataframe"})))

    def publish(self, foundry_metadata, update=False, **kwargs):
        """Submit a data package for publication
        Args:
            foundry_metadata (dict): Path to the file containing
            update (bool): True if this is an update to a prior data package
            (default: self.config.metadata_file)
        Keyword Args:
            title (str): Title of the data package
            authors (list): List of data package author names e.g., Jack Black or Nunez, Victoria
            affiliations (list): List of author affiliations
            tags (list): List of tags to apply to the data package

        Returns
        -------
        (dict) MDF Connect Response: Response from MDF Connect to allow tracking of dataset 
        """

        self.connect_client.create_dc_block(
            title=kwargs["title"],
            authors=kwargs["authors"],
            affiliations=kwargs.get("affiliations", []),
            subjects=kwargs.get("tags", ["machine learning", "foundry"]),
        )
        self.connect_client.add_organization("Foundry")
        self.connect_client.set_project_block("foundry", foundry_metadata)
        self.connect_client.add_data_source(kwargs.get("data_sources", []))

        res = self.connect_client.submit_dataset(update=update)
        return res

    def from_file(self, file=None):
        """Create a Foundry client from a file

        Args:
            file (str): Path to the file containing
            (default: self.config.metadata_file)

        Returns
        -------
        (Foundry): an newly instantiated Foundry client
        """

        if file is None:
            file = self.config.metadata_file
        with open("./{}".format(file)) as fp:
            obj = json.load(fp)
            return Foundry(**obj)

    def to_file(self, file=None):
        """Create a Foundry client from a file

        Args:
            file (str): Path to the file to save metadata to
            (default: self.config.metadata_file)

        Returns
        -------
        (Foundry) self: for chaining
        """

        if file is None:
            file = self.config.metadata_file
        with open("./{}".format(file)) as fp:
            obj = json.dump(self.json(exclude={"dlhub_client", "forge_client"}), fp)
        return self

    def configure(self, **kwargs):
        self.config = FoundryConfig(**kwargs)
        return self

    def download(self, globus=True, **kwargs):
        # Check if the dir already exists
        if os.path.isdir(
            os.path.join(self.config.local_cache_dir, self.mdf["source_id"])
        ):
            return self

        res = self.forge_client.search(
            "mdf.source_id:{name}".format(name=self.mdf["source_id"]), advanced=True
        )
        if globus:
            self.forge_client.globus_download(
                res,
                dest=self.config.local_cache_dir,
                dest_ep=self.config.destination_endpoint,
                interval=kwargs.get("interval", 20),
                download_datasets=True,
            )
        else:
            self.forge_client.http_download(
                res, dest=self.config.local_cache_dir, preserve_dir=True
            )
        return self
