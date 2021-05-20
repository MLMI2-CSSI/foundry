from requests.packages.urllib3.exceptions import InsecureRequestWarning
from foundry.models import (
    FoundryMetadata,
    FoundryConfig,
    FoundrySpecificationDataset,
    FoundrySpecification,
)
from pydantic import AnyUrl, ValidationError
from joblib import Parallel, delayed
from collections import namedtuple
from dlhub_sdk import DLHubClient
# TODO: do imports nicer
from dlhub_sdk.models.servables.sklearn import ScikitLearnModel
from dlhub_sdk.models.servables.keras import KerasModel
from dlhub_sdk.utils.schemas import validate_against_dlhub_schema
from mdf_forge import Forge
from mdf_connect_client import MDFConnectClient
import multiprocessing
from typing import Any
from datetime import date
import multiprocessing
import pandas as pd
import mdf_toolbox
import requests
import json
import glob
import h5py
import time
import os


class Foundry(FoundryMetadata):
    """Foundry Client Base Class
    TODO:
    -------
    Add Docstring

    """

    # transfer_client: Any
    dlhub_client: Any
    forge_client: Any
    connect_client: Any

    xtract_tokens: Any

    def __init__(
        self, no_browser=False, no_local_server=False, search_index="mdf-test", **data
    ):
        super().__init__(**data)
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
            index=search_index,
            services=None,
            search_client=auths["search"],
            transfer_client=auths["transfer"],
            data_mdf_authorizer=auths["data_mdf"],
            petrel_authorizer=auths["petrel"],
        )

        # TODO: when release-ready, remove test=True
        self.connect_client = MDFConnectClient(
            authorizer=auths["mdf_connect"], test=True
        )

        self.dlhub_client = DLHubClient(
            dlh_authorizer=auths["dlhub"],
            search_client=auths["search"],
            fx_authorizer=auths[
                "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all"
            ],
            force_login=False,
        )

        self.xtract_tokens = {
            "auth_token": auths["petrel"].access_token,
            "transfer_token": auths["transfer"].authorizer.access_token,
            "funcx_token": auths[
                "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all"
            ].access_token,
        }

    def load(self, name, version="1.1", provider="MDF", download=True, globus=True, verbose=False, **kwargs,):
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
        res = []
        # MDF specific logic
        # Handle DOI inputs
        if name.startswith("10.") and provider == "MDF":
            print("Loading by DOI")
            res = (
                self.forge_client.match_dois(name)
                .match_resource_types("dataset")
                .match_field("mdf.organizations", "foundry")
                .search()
            )

        # Handle MDF source_ids
        else:
            print("Loading by source_id")
            res = (
                self.forge_client.match_field("mdf.organizations", "foundry")
                .match_resource_types("dataset")
                .match_field("mdf.source_id", name)
                .search()
            )

        if not res:
            return self
        else:
            # res is list of all matches in Forge
            # TODO: handle if there are multiple matches
            res = res[0]
            
            # map result to FoundryMetadata Pydantic structure (see models.py)
            res["dataset"] = res["projects"]["foundry"]
            res["dataset"]["type"] = res["dataset"]["package_type"]
            del res["projects"]["foundry"]

            # TODO: reassign values to self in a safer way
            self = Foundry(**res)

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
            X, y = self.load_data()
            X["source"] = package
            y["source"] = package
            X_frames.append(X)
            y_frames.append(y)

        return pd.concat(X_frames), pd.concat(y_frames)

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
            print("Here")
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
        )
        self.connect_client.add_organization("Foundry")
        self.connect_client.set_project_block("foundry", foundry_metadata)
        self.connect_client.add_data_source(data_source)
        self.connect_client.set_source_name(kwargs.get("short_name", title))

        res = self.connect_client.submit_dataset(update=update)
        return res

    def describe_model(self):
        pass
        # maybe have whole fxn for model describing? tbd

    def publish_model(self, options):
        """Submit a model or function for publication
        Args:
            options: dict of all possible options
        Options keys:
            title (req)
            authors (req)
            short_name (req)
            servable_type (req) ("static method", "class method", "keras", "pytorch", "tensorflow", "sklearn")
            affiliations
            domains
            abstract
            references
            requirements (dict of library:version keypairs)
            module (if Python method)
            function  (if Python method)
            inputs (not needed for TF) (dict of options)
            outputs (not needed for TF)
            methods (e.g. research methods)
            DOI
            publication_year (advanced)
            version (advanced)
            visibility (dict of users and groups, each a list)
            funding reference
            rights

            TODO:
            alternate identifier (to add an identifier of this artifact in another service)
            add file
            add directory
            add files

        """
        # TODO: pick nicer way of handling defaults for things besides get (since if the DLHub default changes, we'd be
        #   overwriting it

        # TODO: add exception handling for key options

        # TODO: make this work for any model type, with if-else
        if options["servable"]["type"] == "sklearn":
            model_info = ScikitLearnModel.create_model(options["servable"]["filepath"],
                                                       options["servable"]["n_input_columns"],
                                                       options["servable"].get("classes", None),
                                                       options["servable"].get("serialization_method", "pickle")
                                                       )
        # TODO: fix weird M1 error with TF
        elif options["servable"]['type'] == "keras":
            model_info = KerasModel.create_model(options["servable"]["model_path"],
                                                 options["servable"].get("output_names", None),
                                                 options["servable"].get("arch_path", None),
                                                 options["servable"].get("custom_objects", None)
                                                 )
        else:
            raise ValueError("Servable type '{}' is not recognized, please use one of the following types: \n"
                             "'sklearn'\n"
                             "'keras'\n"
                             "'pytorch'\n"
                             "'tensorflow'\n"
                             "'static method'\n"
                             "'class method'\n"
                             .format(options["servable"]["type"]))
        # publish it
        model_info.set_name(options["short_name"])
        model_info.set_title(options["title"])
        # TODO: fix bug where if you put in name without comma, get list index out of range error
        model_info.set_authors(options["authors"], options.get("affiliations", []))
        # TODO: dont pass in {} as default, overwrites everything -- should def document this
        # TODO: consider whether that's desired functionality (should users be able to specify 1 or 2 requirements, but
        #   the container still has other pre-loaded dependencies?
        # model_info.add_requirements(options.get("requirements", {}))
        model_info.set_domains(options.get("domains", []))
        # TODO: can't default to empty strings, handle
        # model_info.set_abstract(options.get("abstract", ""))
        # model_info.set_methods(options.get("methods", ""))
        # TODO: ask Ben if user should set this, check what happens if they dont
        # model_info.set_version(kwargs.get("version", ""))

        # TODO: add dict for rights
        # model_info.add_rights()

        # advanced use only (most users will not know DOI)
        if options.get("doi"):
            model_info.set_doi(options.get("doi"))
        # advanced use only
        if options.get("publication_year"):
            model_info.set_publication_year(options.get("publication_year"))

        # TODO: parse dict of lists
        # model_info.set_visibility()

        # TODO: parse dict of references (need to loop)
        # model_info.add_related_identifier()

        # TODO: parse dict of options (need to loop)
        # model_info.add_funding_reference()

        # TODO: pass dict of data_type, description, shape (opt), item_type (opt) and kwargs
        # model_info.set_inputs()
        # model_info.set_outputs()

        try:
            validate_against_dlhub_schema(model_info.to_dict(), 'servable')
            print("DLHub schema successfully validated")
        except Exception as e:
            print("Failed to validate schema properly: {}".format(e))
            raise e

        res = self.dlhub_client.publish_servable(model_info)

        return res

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

    def check_model_status(self, res):
        """Check status of model or function publication to DLHub

        TODO: currently broken on DLHub side of things
        """
        # return self.dlhub_client.get_task_status(res)
        pass

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
            source_id = self.mdf["source_id"]
            xtract_base_url = (
                "http://xtract-crawler-4.eba-ghixpmdf.us-east-1.elasticbeanstalk.com"
            )

            # MDF Materials Data at NCSA
            source_ep_id = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec"
            base_url = "https://data.materialsdatafacility.org"
            folder_to_crawl = f"/foundry/{source_id}/"

            # This only matters if you want files grouped together.
            grouper = "matio"

            auth_token = self.xtract_tokens["auth_token"]
            transfer_token = self.xtract_tokens["transfer_token"]
            funcx_token = self.xtract_tokens["funcx_token"]

            headers = {
                "Authorization": auth_token,
                "Transfer": transfer_token,
                "FuncX": funcx_token,
                "Petrel": auth_token,
            }
            if verbose:
                print(f"Headers: {headers}")

            # Initialize the crawl. This kicks off the Globus EP crawling service on the backend.
            crawl_url = f"{xtract_base_url}/crawl"
            if verbose:
                print(f"Crawl URL is : {crawl_url}")

            first_ep_dict = {
                "repo_type": "GLOBUS",
                "eid": source_ep_id,
                "dir_paths": [folder_to_crawl],
                "grouper": grouper,
            }
            tokens = {"Transfer": transfer_token, "Authorization": funcx_token}
            crawl_req = requests.post(
                f"{xtract_base_url}/crawl",
                json={"endpoints": [first_ep_dict], "tokens": tokens},
            )

            if verbose:
                print("Crawl response:", crawl_req)
            crawl_id = json.loads(crawl_req.content)["crawl_id"]
            if verbose:
                print(f"Crawl ID: {crawl_id}")

            # Wait for the crawl to finish before we can start fetching our metadata.
            while True:
                crawl_status = requests.get(
                    f"{xtract_base_url}/get_crawl_status", json={"crawl_id": crawl_id}
                )
                if verbose:
                    print(crawl_status)
                crawl_content = json.loads(crawl_status.content)
                if verbose:
                    print(f"Crawl Status: {crawl_content}")

                if crawl_content["crawl_status"] == "complete":
                    files_crawled = crawl_content["files_crawled"]
                    if verbose:
                        print("Our crawl has succeeded!")
                    break
                else:
                    if verbose:
                        print("Sleeping before re-polling...")
                    time.sleep(2)

            # Now we fetch our metadata. Here you can configure n to be maximum number of
            # messages you want at once.

            file_ls = []
            fetched_files = 0
            while fetched_files < files_crawled:
                fetch_mdata = requests.get(
                    f"{xtract_base_url}/fetch_crawl_mdata",
                    json={"crawl_id": crawl_id, "n": 2},
                )
                fetch_content = json.loads(fetch_mdata.content)

                for file_path in fetch_content["file_ls"]:
                    file_ls.append(file_path)
                    fetched_files += 1

                if fetch_content["queue_empty"]:
                    if verbose:
                        print("Queue is empty! Continuing...")
                    time.sleep(2)

            source_path = os.path.join(
                self.config.local_cache_dir, self.mdf["source_id"]
            )

            if not os.path.exists(self.config.local_cache_dir):
                os.mkdir(self.config.local_cache_dir)
                os.mkdir(source_path)

            elif not os.path.exists(source_path):
                os.mkdir(source_path)

            num_cores = multiprocessing.cpu_count()

            def download_file(file):
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

                url = "https://data.materialsdatafacility.org" + file["path"]
                destination = (
                    "data/"
                    + source_id
                    + "/"
                    + file["path"][file["path"].rindex("/") + 1 :]
                )
                response = requests.get(url, verify=False)

                with open(destination, "wb") as f:
                    f.write(response.content)

                return {file["path"] + " status": True}

            results = Parallel(n_jobs=num_cores)(
                delayed(download_file)(file) for file in file_ls
            )

            print("Done curling.")
            print(results)

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

        print("Building Data Package")
        num_cores = multiprocessing.cpu_count()

        def start_download(ds, interval=interval, globus=False):
            print("=== Fetching Data Package {} ===".format(ds.name))
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
