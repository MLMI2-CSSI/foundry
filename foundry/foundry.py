
from foundry.xtract_method import *
import time
import h5py
import glob
import json
import requests
import mdf_toolbox
from json2table import convert
import pandas as pd
from datetime import date
from typing import Any
import multiprocessing
from mdf_connect_client import MDFConnectClient
from mdf_forge import Forge
# from dlhub_sdk.utils.schemas import validate_against_dlhub_schema
# from dlhub_sdk.models.servables.keras import KerasModel
# from dlhub_sdk.models.servables.sklearn import ScikitLearnModel
# from dlhub_sdk import DLHubClient
from collections import namedtuple
from joblib import Parallel, delayed
from pydantic import AnyUrl, ValidationError
from foundry.models import (
    FoundryMetadata,
    FoundryConfig,
    FoundrySpecificationDataset,
    FoundrySpecification,
    FoundryDataset
)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
import os
import shutil
logging.disable(logging.INFO)


class Foundry(FoundryMetadata):
    """Foundry Client Base Class
    TODO:
    -------
    Add Docstring

    """

    # transfer_client: Any
    # dlhub_client: Any
    forge_client: Any
    connect_client: Any
    index = ""

    xtract_tokens: Any

    def __init__(
        self, no_browser=False, no_local_server=False, index="mdf-test", authorizers=None, **data
    ):
        """Initialize a Foundry client
        Args:
            no_browser (bool):  Whether to open the browser for the Globus Auth URL.
            no_local_server (bool): Whether a local server is available.
                    This should be `False` when on remote server (e.g., Google Colab ).
            index (str): Index to use for search and data publication. Choices `mdf` or `mdf-test`
            authorizers (dict): A dictionary of authorizers to use, following the `mdf_toolbox` format
            data (dict): Other arguments, e.g., results from an MDF search result that are used
                    to populate Foundry metadata fields

        Returns
        -------
            an initialized and authenticated Foundry client
        """
        super().__init__(**data)
        self.index = index

        if authorizers:
            auths = authorizers
        else:
            auths = mdf_toolbox.login(
                services=[
                    "data_mdf",
                    "mdf_connect",
                    "search",
                    "petrel",
                    "transfer",
                    "dlhub",
                    "openid",
                    "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all",
                ],
                app_name="Foundry",
                make_clients=True,
                no_browser=no_browser,
                no_local_server=no_local_server,
            )

        self.forge_client = Forge(
            index=index,
            services=None,
            search_client=auths["search"],
            transfer_client=auths["transfer"],
            data_mdf_authorizer=auths["data_mdf"],
            petrel_authorizer=auths["petrel"],
        )

        if index == "mdf":
            test = False
        else:
            test = True
        # TODO: when release-ready, remove test=True

        self.connect_client = MDFConnectClient(
            authorizer=auths["mdf_connect"], test=test
        )

        ## TODO: come back to add in DLHub functionality after globus-sdk>=3.0 supported
        # self.dlhub_client = DLHubClient(
        #     dlh_authorizer=auths["dlhub"],
        #     search_client=auths["search"],
        #     fx_authorizer=auths[
        #         "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all"
        #     ],
        #     openid_authorizer=auths['openid'],
        #     force_login=False,
        # )


        self.xtract_tokens = {
            "auth_token": auths["petrel"].access_token,
            "transfer_token": auths["transfer"].authorizer.access_token,
            "funcx_token": auths[
                "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all"
            ].access_token,
        }

    def load(self, name, download=True, globus=True, verbose=False, metadata=None, authorizers=None, **kwargs):
        """Load the metadata for a Foundry dataset into the client
        Args:
            name (str): Name of the foundry dataset
            download (bool): If True, download the data associated with the package (default is True)
            globus (bool): If True, download using Globus, otherwise https
            verbose (bool): If True print additional debug information
            metadata (dict): **For debug purposes.** A search result analog to prepopulate metadata.

        Keyword Args:
            interval (int): How often to poll Globus to check if transfers are complete

        Returns
        -------
            self
        """

        # handle empty dataset name (was returning all the datasets)
        if not name:
            raise ValueError("load: No dataset name is given")

        if metadata:
            res = metadata

        if metadata:
            res = metadata

        # MDF specific logic
        if is_doi(name) and not metadata:
            res = self.forge_client.match_resource_types("dataset")
            res = res.match_dois(name).search()

        else:
            res = self.forge_client.match_field(
                "mdf.organizations", self.config.organization
            ).match_resource_types("dataset")
            res = res.match_field("mdf.source_id", name).search()

        # unpack res, handle if empty
        try:
            # if search returns multiple results, this automatically uses first result
            res = res[0]
        except IndexError as e:
            raise Exception("load: No metadata found for given dataset") from e

        try:
            res["dataset"] = res["projects"][self.config.metadata_key]
        except KeyError as e:
            raise Exception(f"load: not able to index with metadata key {self.config.metadata_key}") from e

        del res["projects"][self.config.metadata_key]

        # TODO: Creating a new Foundry instance is a problematic way to update the metadata,
        # we should find a way to abstract this.

        fdataset = FoundryDataset(**res['dataset'])
        self.dc = res['dc']
        self.mdf = res['mdf']
        self.dataset = fdataset


        if download is True:  # Add check for package existence
            self.download(
                interval=kwargs.get("interval", 10), globus=globus, verbose=verbose
            )

        return self

    def list(self):
        """List available Foundry data packages

        Returns
        -------
            (pandas.DataFrame): DataFrame with summary list of Foundry data packages including name, title, and publication year
        """
        res = (
            self.forge_client.match_field(
                "mdf.organizations", self.config.organization)
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

    def collect_dataframes(self, packages=[]):
        """Collect dataframes of local data packages
        Args:
           packages (list): List of packages to collect, defaults to all

        Returns
        -------
            (tuple): Tuple of X(pandas.DataFrame), y(pandas.DataFrame)
        """
        if not packages:
            packages = self.get_packages()
        f = Foundry()

        X_frames = []
        y_frames = []

        for package in packages:
            self = self.load(package)
            X, y = self.load_data()  # TODO: update how this is unpacked, out of date
            X["source"] = package
            y["source"] = package
            X_frames.append(X)
            y_frames.append(y)

        return pd.concat(X_frames), pd.concat(y_frames)

    # def run(self, name, inputs, **kwargs):
    #     """Run a model on data
    #
    #     Args:
    #        name (str): DLHub model name
    #        inputs: Data to send to DLHub as inputs (should be JSON serializable)
    #
    #     Returns
    #     -------
    #          Returns results after invocation via the DLHub service
    #
    #     TODO:
    #     -------
    #     - Pass **kwargs through to DLHub client and document kwargs
    #     """
    #     return self.dlhub_client.run(name, inputs=inputs)

    def load_data(self, source_id=None, globus=True):
        """Load in the data associated with the prescribed dataset

        Tabular Data Type: Data are arranged in a standard data frame
        stored in self.dataframe_file. The contents are read, and

        File Data Type: <<Add desc>>

        For more complicated data structures, users should
        subclass Foundry and override the load_data function

        Args:
           inputs (list): List of strings for input columns
           targets (list): List of strings for output columns

        Returns
        -------s
             (tuple): Tuple of X, y values
        """
        data = {}

        # Handle splits if they exist. Return as a labeled dictionary of tuples
        try:
            if self.dataset.splits:
                for split in self.dataset.splits:
                    data[split.label] = self._load_data(file=split.path,
                                                        source_id=source_id, globus=globus)
                return data
            else:
                return {"data": self._load_data(source_id=source_id, globus=globus)}
        except Exception as e:
            raise Exception(
                "Metadata not loaded into Foundry object, make sure to call load()") from e

    def _repr_html_(self) -> str:
        if not self.dc:
            buf = str(self)
        else:
            title = self.dc['titles'][0]['title']
            authors = [creator['creatorName']
                       for creator in self.dc['creators']]
            authors = '; '.join(authors)

            buf = f'<h2>{title}</h2>{authors}'

            buf = f'{buf}<h3>Dataset</h3>{convert(json.loads(self.dataset.json(exclude={"dataframe"})))}'
        # buf = f'{buf}<h3>MDF</h3>{convert(self.mdf)}'
        # buf = f'{buf}<h3>DataCite</h3>{convert(self.dc)}'
        return buf

    def publish(self, foundry_metadata, data_source, title, authors, update=False,
                publication_year=None, **kwargs,):
        """Submit a dataset for publication
        Args:
            foundry_metadata (dict): Dict of metadata describing data package
            data_source (string): Url for Globus endpoint
            title (string): Title of data package
            authors (list): List of data package author names e.g., Jack Black
                or Nunez, Victoria
            update (bool): True if this is an update to a prior data package
                (default: self.config.metadata_file)
            publication_year (int): Year of dataset publication. If None, will
                be set to the current calendar year by MDF Connect Client.
                (default: $current_year)

        Keyword Args:
            affiliations (list): List of author affiliations
            tags (list): List of tags to apply to the data package
            short_name (string): Shortened/abbreviated name of the data package
            publisher (string): Data publishing entity (e.g. MDF, Zenodo, etc.)
            description (str): A description of the dataset.
            dataset_doi (str): The DOI for this dataset (not an associated paper).
            related_dois (list): DOIs related to this dataset,
                    not including the dataset's own DOI (for example, an associated paper's DOI).

        Returns
        -------
        (dict) MDF Connect Response: Response from MDF Connect to allow tracking
            of dataset. Contains `source_id`, which can be used to check the
            status of the submission
        """
        self.connect_client.create_dc_block(
            title=title,
            authors=authors,
            affiliations=kwargs.get("affiliations", []),
            subjects=kwargs.get("tags", ["machine learning", "foundry"]),
            publisher=kwargs.get("publisher", ""),
            publication_year=publication_year,
            description=kwargs.get("description", ""),
            dataset_doi=kwargs.get("dataset_doi", ""),
            related_dois=kwargs.get("related_dois", [])
        )
        self.connect_client.add_organization(self.config.organization)
        self.connect_client.set_project_block(
            self.config.metadata_key, foundry_metadata)
        self.connect_client.add_data_source(data_source)
        self.connect_client.set_source_name(kwargs.get("short_name", title))

        res = self.connect_client.submit_dataset(update=update)
        return res

    # TODO: come back and address DLHub code
    #
    # def describe_model(self):
    #     pass
    #     # maybe have whole fxn for model describing? tbd
    #
    # def publish_model(self, options):
    #     """Submit a model or function for publication
    #     Args:
    #         options: dict of all possible options
    #     Options keys:
    #         title (req)
    #         authors (req)
    #         short_name (req)
    #         servable_type (req) ("static method", "class method",
    #                        "keras", "pytorch", "tensorflow", "sklearn")
    #         affiliations
    #         domains
    #         abstract
    #         references
    #         requirements (dict of library:version keypairs)
    #         module (if Python method)
    #         function  (if Python method)
    #         inputs (not needed for TF) (dict of options)
    #         outputs (not needed for TF)
    #         methods (e.g. research methods)
    #         DOI
    #         publication_year (advanced)
    #         version (advanced)
    #         visibility (dict of users and groups, each a list)
    #         funding reference
    #         rights
    #
    #         TODO:
    #         alternate identifier (to add an identifier of this artifact in another service)
    #         add file
    #         add directory
    #         add files
    #
    #     """
    #     # TODO: pick nicer way of handling defaults for things besides get (since if the DLHub default changes, we'd be
    #     #   overwriting it
    #
    #     # TODO: add exception handling for key options
    #
    #     # TODO: make this work for any model type, with if-else
    #     if options["servable"]["type"] == "sklearn":
    #         model_info = ScikitLearnModel.create_model(options["servable"]["filepath"],
    #                                                    options["servable"]["n_input_columns"],
    #                                                    options["servable"].get(
    #                                                        "classes", None),
    #                                                    options["servable"].get(
    #                                                        "serialization_method", "pickle")
    #                                                    )
    #     # TODO: fix weird M1 error with TF
    #     elif options["servable"]['type'] == "keras":
    #         model_info = KerasModel.create_model(options["servable"]["model_path"],
    #                                              options["servable"].get(
    #                                                  "output_names", None),
    #                                              options["servable"].get(
    #                                                  "arch_path", None),
    #                                              options["servable"].get(
    #                                                  "custom_objects", None),
    #                                              options["servable"].get(
    #                                                  "force_tf_keras", False)
    #                                              )
    #     else:
    #         raise ValueError("Servable type '{}' is not recognized, please use one of the following types: \n"
    #                          "'sklearn'\n"
    #                          "'keras'\n"
    #                          "'pytorch'\n"
    #                          "'tensorflow'\n"
    #                          "'static method'\n"
    #                          "'class method'\n"
    #                          .format(options["servable"]["type"]))
    #     # publish it
    #     model_info.set_name(options["short_name"])
    #     model_info.set_title(options["title"])
    #     # TODO: fix bug where if you put in name without comma, get list index out of range error
    #     model_info.set_authors(
    #         options["authors"], options.get("affiliations", []))
    #     # TODO: dont pass in {} as default, overwrites everything -- should def document this
    #     # TODO: consider whether that's desired functionality (should users be able to specify 1 or 2 requirements, but
    #     #   the container still has other pre-loaded dependencies?
    #     # model_info.add_requirements(options.get("requirements", {}))
    #     model_info.set_domains(options.get("domains", []))
    #     # TODO: can't default to empty strings, handle
    #     # model_info.set_abstract(options.get("abstract", ""))
    #     # model_info.set_methods(options.get("methods", ""))
    #     # TODO: ask Ben if user should set this, check what happens if they dont
    #     # model_info.set_version(kwargs.get("version", ""))
    #
    #     # TODO: add dict for rights
    #     # model_info.add_rights()
    #
    #     # advanced use only (most users will not know DOI)
    #     if options.get("doi"):
    #         model_info.set_doi(options.get("doi"))
    #     # advanced use only
    #     if options.get("publication_year"):
    #         model_info.set_publication_year(options.get("publication_year"))
    #
    #     # TODO: parse dict of lists
    #     # model_info.set_visibility()
    #
    #     # TODO: parse dict of references (need to loop)
    #     # model_info.add_related_identifier()
    #
    #     # TODO: parse dict of options (need to loop)
    #     # model_info.add_funding_reference()
    #
    #     # TODO: pass dict of data_type, description, shape (opt), item_type (opt) and kwargs
    #     # model_info.set_inputs()
    #     # model_info.set_outputs()
    #
    #     try:
    #         validate_against_dlhub_schema(model_info.to_dict(), 'servable')
    #         print("DLHub schema successfully validated")
    #     except Exception as e:
    #         print("Failed to validate schema properly: {}".format(e))
    #         raise e
    #
    #     res = self.dlhub_client.publish_servable(model_info)
    #
    #     return res

    def check_status(self, source_id, short=False, raw=False):
        """Check the status of your submission.

        Arguments:
            source_id (str): The ``source_id`` (``source_name`` + version information) of the
                    submission to check. Returned in the ``res`` result from ``publish()`` via MDF Connect Client.
            short (bool): When ``False``, will print a status summary containing
                    all of the status steps for the dataset.
                    When ``True``, will print a short finished/processing message,
                    useful for checking many datasets' status at once.
                    **Default:** ``False``
            raw (bool): When ``False``, will print a nicely-formatted status summary.
                    When ``True``, will return the full status result.
                    For direct human consumption, ``False`` is recommended.
                    **Default:** ``False``

        Returns:
            If ``raw`` is ``True``, *dict*: The full status result.
        """
        return self.connect_client.check_status(source_id, short, raw)

    # def check_model_status(self, res):
    #     """Check status of model or function publication to DLHub
    #
    #     TODO: currently broken on DLHub side of things
    #     """
    #     # return self.dlhub_client.get_task_status(res)
    #     pass

    def configure(self, **kwargs):
        """Set Foundry config
        Keyword Args:
            file (str): Path to the file containing
            (default: self.config.metadata_file)

        dataframe_file (str): filename for the dataframe file default:"foundry_dataframe.json"
        data_file (str): : filename for the data file default:"foundry.hdf5"
        destination_endpoint (str): Globus endpoint UUID where Foundry data should move
        local_cache_dir (str): Where to place collected data default:"./data"

        Returns
        -------
        (Foundry): self: for chaining
        """
        self.config = FoundryConfig(**kwargs)
        return self

    def download(self, globus=True, verbose=False, **kwargs):
        """Download a Foundry dataset
        Args:
            globus (bool): if True, use Globus to download the data else try HTTPS
            verbose (bool): if True print out debug information during the download

        Returns
        -------
        (Foundry): self: for chaining
        """
        # Check if the dir already exists
        path = os.path.join(self.config.local_cache_dir, self.mdf["source_id"])

        if os.path.isdir(path):
            # if directory is present, but doesn't have the correct number of files inside,
            # dataset will attempt to redownload
            if self.dataset.splits:
                # array to keep track of missing files
                missing_files = []
                for split in self.dataset.splits:
                    if split.path[0] == '/':
                        split.path = split.path[1:]
                    if not os.path.isfile(os.path.join(path, split.path)):
                        missing_files.append(split.path)
                #if number of missing files is greater than zero, redownload with informative message
                if len(missing_files) > 0:
                    print(f"Dataset will be redownloaded, following files are missing: {missing_files}")
                else:
                    return self
            else:
                # in the case of no splits, ensure the directory contains at least one file
                if(len(os.listdir(path)) >= 1):
                    return self
                else:
                    print("Dataset will be redownloaded, expected file is missing")

        res = self.forge_client.search(
            f"mdf.source_id:{self.mdf['source_id']}", advanced=True
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

            source_id = self.mdf["source_id"]
            xtract_config = {
                 "xtract_base_url": "http://xtractcrawler5-env.eba-akbhvznm.us-east-1.elasticbeanstalk.com/",
                 "source_ep_id": "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec",
                 "base_url": "https://data.materialsdatafacility.org",
                 "folder_to_crawl": f"/foundry/{source_id}/",
                 "grouper": "matio"
                }
            xtract_https_download(self, verbose=verbose, **xtract_config) # TODO: figure out better way than passing self?

        # after download check making sure directory exists, contains all indicated files
        if os.path.isdir(path):
            # checking all necessary files are present
            if self.dataset.splits:
                missing_files = []
                for split in self.dataset.splits:
                    if split.path[0] == '/': # if absolute path, make it a relative path
                        split.path = split.path[1:]
                    if not os.path.isfile(os.path.join(path, split.path)):
                        # keeping track of all files not downloaded
                        missing_files.append(split.path)
                if len(missing_files) > 0:
                    raise FileNotFoundError(f"Downloaded directory does not contain the following files: {missing_files}")

            else:
                if(len(os.listdir(path)) < 1):
                    raise FileNotFoundError("Downloaded directory does not contain the expected file")
        else:
            raise NotADirectoryError("Unable to create directory to download data")

        return self

    def build(self, spec, globus=False, interval=3, file=False):
        """Build a Foundry Data Package
        Args:
            spec (multiple): dict or str (relative filename) of the data package specification
            globus (bool): if True use Globus to fetch datasets
            interval (int): Polling interval on checking task status in seconds.
            type (str): One of "file" or None

        Returns
        -------
        (Foundry): self: for chaining
        """
        if as_object:
            return [key for key in self.dataset.keys if key.type == type]
        else:
            keys = [key.key for key in self.dataset.keys if key.type == type]
            key_list = []
            for k in keys:
                key_list = key_list + k
            return key_list

        print("Building Data Package")
        num_cores = multiprocessing.cpu_count()

        def start_download(ds, interval=interval, globus=False):
            print(f"=== Fetching Data Package {ds.name} ===")
            f = Foundry().load(ds.name, download=False)
            f = f.download(interval=interval, globus=globus)
            return {"success": True}

        if file:
            with open(file, "r") as fp:
                fs = FoundrySpecification(**json.load(fp))
        else:
            fs = FoundrySpecification(**spec)

        fs.remove_duplicate_dependencies()

        results = Parallel(n_jobs=num_cores)(
            delayed(start_download)(ds, interval=interval, globus=globus)
            for ds in fs.dependencies
        )

        return self

    def get_keys(self, type=None, as_object=False):
        """Get keys for a Foundry dataset

        Arguments:
            type (str): The type of key to be returned e.g., "input", "target"
            as_object (bool): When ``False``, will return a list of keys in as strings
                    When ``True``, will return the full key objects
                    **Default:** ``False``
        Returns: (list) String representations of keys or if ``as_object``
                    is False otherwise returns the full key objects.

        """

        if as_object:
            if type:
                return [key for key in self.dataset.keys if key.type == type]
            else:
                return [key for key in self.dataset.keys]

        else:
            if type:
                keys = [key.key for key in self.dataset.keys if key.type == type]
            else:
                keys = [key.key for key in self.dataset.keys]

            key_list = []
            for k in keys:
                key_list = key_list + k
            return key_list


    def _load_data(self, file=None, source_id=None, globus=True):

        # Build the path to access the cached data
        if source_id:
            path = os.path.join(self.config.local_cache_dir, source_id)
        else:
            path = os.path.join(self.config.local_cache_dir,
                                self.mdf["source_id"])

        # Handle Foundry-defined types.
        if self.dataset.data_type.value == "tabular":
            # Determine which file to load, defaults to config.dataframe_file
            if not file:
                file = self.config.dataframe_file


            # Check to make sure the path can be created
            try:
                path_to_file = os.path.join(path, file)
            except Exception as e:
                print(f"Unable to find path to file for download: {e}")
                raise e

            # Check to see whether file exists at path
            if not os.path.isfile(path_to_file):
                raise FileNotFoundError(f"No file found at expected path: {path_to_file}")
            # If the file is not local, fetch the contents with Globus
            # Check if the contents are local
            # TODO: Add hashes and versioning to metadata and checking to the file
            try:
                self.dataset.dataframe = pd.read_json(
                    path_to_file
                )
            except Exception as e:
                print(f"Reading {file} as JSON failed: {e} \n", "Now attempting to read as JSONL")
                try:
                    # Try to read individual lines instead
                    self.dataset.dataframe = pd.read_json(
                        path_to_file, lines=True
                    )
                except Exception as f:
                    print(f"Reading {file} as JSONL failed: {f} \n", "Now attempting to read as CSV")
                    try:
                        #Try to read as CSV instead
                        self.dataset.dataframe = pd.read_csv(
                            path_to_file
                        )
                    except Exception as g:
                        print(f"Reading {file} as CSV failed, unable to load data properly: {g}")
                        raise e

            return (
                self.dataset.dataframe[self.get_keys("input")],
                self.dataset.dataframe[self.get_keys("target")],
            )

        elif self.dataset.data_type.value == "hdf5":
            if not file:
                file = self.config.data_file

            filepath = os.path.join(path, file)
            f = h5py.File(filepath, "r")
            special_types = ["input", "target"]
            tmp_data = {s: {} for s in special_types}
            for s in special_types:
                for key in self.get_keys(s):
                    if isinstance(f[key], h5py.Group):
                        if is_pandas_pytable(f[key]):
                            df = pd.read_hdf(filepath, key)
                            tmp_data[s][key] = df
                        else:
                            tmp_data[s][key] = f[key]
                    elif isinstance(f[key], h5py.Dataset):
                        tmp_data[s][key] = f[key][0:]
            return tmp_data
        else:
            raise NotImplementedError


def is_pandas_pytable(group):
    if 'axis0' in group.keys() and 'axis1' in group.keys():
        return True
    else:
        return False


def is_doi(string: str):
    if string.startswith('10.') or string.startswith('https://doi.org/'):
        return True
    else:
        return False
