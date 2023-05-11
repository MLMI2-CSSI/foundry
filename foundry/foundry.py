import h5py
import json
import mdf_toolbox
from json2table import convert
import numpy as np
import pandas as pd
from typing import Any, Dict, List
import logging
import warnings
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm

from mdf_connect_client import MDFConnectClient
from mdf_forge import Forge
from dlhub_sdk import DLHubClient
from globus_sdk import AuthClient

from .auth import PubAuths
from .utils import is_pandas_pytable, is_doi
from .utils import _read_csv, _read_json, _read_excel

from foundry.models import (
    FoundryMetadata,
    FoundryConfig,
    FoundryDataset
)
from foundry.https_download import download_file, recursive_ls
from foundry.https_upload import upload_to_endpoint

logger = logging.getLogger(__name__)


class Foundry(FoundryMetadata):
    """Foundry Client Base Class
    TODO:
    -------
    Add Docstring

    """

    dlhub_client: Any
    forge_client: Any
    connect_client: Any
    transfer_client: Any
    auth_client: Any
    index = ""
    auths: Any

    xtract_tokens: Any

    def __init__(
            self, no_browser=False, no_local_server=False, index="mdf", authorizers=None, **data
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
        self.auths = None

        if authorizers:
            self.auths = authorizers
        else:
            services = [
                    "data_mdf",
                    "mdf_connect",
                    "search",
                    "petrel",
                    "transfer",
                    "dlhub",
                    "openid",
                    "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all",  # funcx
                    "https://auth.globus.org/scopes/f10a69a9-338c-4e5b-baa1-0dc92359ab47/https",  # Eagle HTTPS
                    "https://auth.globus.org/scopes/82f1b5c6-6e9b-11e5-ba47-22000b92c6ec/https",  # NCSA HTTPS
                    "https://auth.globus.org/scopes/d31d4f5d-be37-4adc-a761-2f716b7af105/action_all",  # Globus Search Lambda
                ]
            self.auths = mdf_toolbox.login(
                services=services,
                app_name="Foundry",
                make_clients=True,
                no_browser=no_browser,
                no_local_server=no_local_server,
            )
            # request Search as an authorizer and not a client
            search_auth = mdf_toolbox.login(
                services=['search'],
                app_name="Foundry",
                make_clients=False,
                no_browser=no_browser,
                no_local_server=no_local_server,
            )
            # add special SearchAuthorizer object
            self.auths['search_authorizer'] = search_auth['search']

        self.forge_client = Forge(
            index=index,
            services=None,
            search_client=self.auths["search"],
            transfer_client=self.auths["transfer"],
            data_mdf_authorizer=self.auths["data_mdf"],
            petrel_authorizer=self.auths["petrel"],
        )

        self.transfer_client = self.auths['transfer']

        self.auth_client = AuthClient(authorizer=self.auths['openid'])

        if index == "mdf":
            test = False
        else:
            test = True
        # TODO: when release-ready, remove test=True

        self.connect_client = MDFConnectClient(
            authorizer=self.auths["mdf_connect"], test=test
        )

        self.dlhub_client = DLHubClient(
            dlh_authorizer=self.auths["dlhub"],
            search_authorizer=self.auths["search_authorizer"],
            fx_authorizer=self.auths[
                "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all"
            ],
            openid_authorizer=self.auths['openid'],
            sl_authorizer=self.auths[
                "https://auth.globus.org/scopes/d31d4f5d-be37-4adc-a761-2f716b7af105/action_all"
            ],
            force_login=False,
        )

        self.xtract_tokens = {
            "auth_token": self.auths["petrel"].access_token,
            "transfer_token": self.auths["transfer"].authorizer.access_token,
            "funcx_token": self.auths[
                "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all"
            ].access_token,
        }

    def load(self, name, download=True, globus=False, verbose=False, metadata=None, authorizers=None, **kwargs):
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
        if len(res) == 0:
            raise Exception(f"load: No metadata found for given dataset {name}")

        # if search returns multiple results, this automatically uses first result, while warning the user
        if len(res) > 1:
            warnings.warn("Multiple datasets found for the given search query. Using first dataset")
        res = res[0]

        try:
            res["dataset"] = res["projects"][self.config.metadata_key]
        except KeyError as e:
            raise Exception(f"load: not able to index with metadata key {self.config.metadata_key}") from e

        del res["projects"][self.config.metadata_key]

        # TODO: Creating a new Foundry instance is a problematic way to update the metadata,
        # we should find a way to abstract this.

        self.dc = res['dc']
        self.mdf = res['mdf']
        self.dataset = FoundryDataset(**res['dataset'])

        if download:  # Add check for package existence
            self.download(
                interval=kwargs.get("interval", 10), globus=globus, verbose=verbose
            )

        return self

    def search(self, q=None, limit=None):
        """Search available Foundry datasets
        q (str): query string to match
        limit (int): maximum number of results to return

        Returns
        -------
            (pandas.DataFrame): DataFrame with summary list of Foundry data packages including name, title, publication year, and DOI
        """
        if not q:
            q = None
        res = (
            self.forge_client.match_field(
                "mdf.organizations", self.config.organization)
            .match_resource_types("dataset")
            .search(q, limit=limit)
        )

        return pd.DataFrame(
            [
                {
                    "source_id": r["mdf"]["source_id"],
                    "name": r["dc"]["titles"][0]["title"],
                    "year": r["dc"].get("publicationYear", None),
                    "DOI": r["dc"].get("identifier", {}).get("identifier", None),
                }
                for r in res
            ]
        )

    def list(self):
        """List available Foundry datasets
        Returns
        -------
            (pandas.DataFrame): DataFrame with summary list of Foundry datasets including name, title, publication year, and DOI
        """
        return self.search()

    def run(self, name, inputs, funcx_endpoint=None, **kwargs):
        """Run a model on data

        Args:
           name (str): DLHub model name
           inputs: Data to send to DLHub as inputs (should be JSON serializable)
           funcx_endpoint (optional): UUID for the funcx endpoint to run the model on, if not the default (eg River)

        Returns
        -------
             Returns results after invocation via the DLHub service
        """
        if funcx_endpoint is not None:
            self.dlhub_client.fx_endpoint = funcx_endpoint
        return self.dlhub_client.run(name, inputs=inputs, **kwargs)

    def load_data(self, source_id=None, globus=True, as_hdf5=False):
        """Load in the data associated with the prescribed dataset

        Tabular Data Type: Data are arranged in a standard data frame
        stored in self.dataframe_file. The contents are read, and

        File Data Type: <<Add desc>>

        For more complicated data structures, users should
        subclass Foundry and override the load_data function

        Args:
           inputs (list): List of strings for input columns
           targets (list): List of strings for output columns
           source_id (string): Relative path to the source file
           as_hdf5 (bool): If True and dataset is in hdf5 format, keep data in hdf5 format

        Returns
        -------
             (tuple): Tuple of X, y values
        """
        data = {}

        # Handle splits if they exist. Return as a labeled dictionary of tuples
        try:
            if self.dataset.splits:
                for split in self.dataset.splits:
                    data[split.label] = self._load_data(file=split.path, source_id=source_id, globus=globus,
                                                        as_hdf5=as_hdf5)
                return data
            else:
                return {"data": self._load_data(source_id=source_id, globus=globus, as_hdf5=as_hdf5)}
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
            DOI = "DOI: " + self.dc['identifier']['identifier']

            buf = f'<h2>{title}</h2>{authors}<p>{DOI}</p>'

            buf = f'{buf}<h3>Dataset</h3>{convert(json.loads(self.dataset.json(exclude={"dataframe"})))}'
        return buf

    def get_citation(self) -> str:
        subjects = [subject['subject'] for subject in self.dc['subjects']]
        doi_str = f"doi = {{{self.dc['identifier']['identifier']}}}"
        url_str = f"url = {{https://doi.org/{self.dc['identifier']['identifier']}}}"
        author_str = f"author = {{{' and '.join([creator['creatorName'] for creator in self.dc['creators']])}}}"
        title_str = f"title = {{{self.dc['titles'][0]['title']}}}"
        keywords_str = f"keywords = {{{', '.join(subjects)}}}"
        publisher_str = f"publisher = {{{self.dc['publisher']}}}"
        year_str = f"year = {{{self.dc['publicationYear']}}}"
        bibtex = os.linesep.join([doi_str, url_str,
                                  author_str, title_str,
                                  keywords_str, publisher_str,
                                  year_str])
        bibtex = f"@misc{{https://doi.org/{self.dc['identifier']['identifier']}{os.linesep}{bibtex}}}"
        return bibtex

    def publish_dataset(
            self, foundry_metadata: Dict[str, Any], title: str, authors: List[str], https_data_path: str = None,
            globus_data_source: str = None, update: bool = False, publication_year: int = None, test: bool = False,
            **kwargs: Dict[str, Any],) -> Dict[str, Any]:
        """Submit a dataset for publication; can choose to submit via HTTPS using `https_data_path` or via Globus
            Transfer using the `globus_data_source` argument. Only one upload method may be specified.
        Args:
            foundry_metadata (dict): Dict of metadata describing data package
            title (string): Title of data package
            authors (list): List of data package author names e.g., Jack Black
                or Nunez, Victoria
            https_data_path (str): Path to the local dataset to publish to Foundry via HTTPS. Creates an HTTPS PUT
                request to upload the data specified to a Globus endpoint (default is NCSA endpoint) before it is
                transferred to MDF. If None, the user must specify a 'globus_data_source' URL to the location of the
                data on their own Globus endpoint. User must choose either `globus_data_source` or `https_data_path` to
                publish their data.
            globus_data_source (str): Url path for a data folder on a Globus endpoint; url can be obtained through
                the Globus Web UI or SDK. If None, the user must specify an 'https_data_path' pointing to the location
                of the data on their local machine. User must choose either `globus_data_source` or `https_data_path` to
                publish their data.
            update (bool): True if this is an update to a prior data package
                (default: self.config.metadata_file)
            publication_year (int): Year of dataset publication. If None, will
                be set to the current calendar year by MDF Connect Client.
                (default: $current_year)
            test (bool): If True, do not submit the dataset for publication (ie transfer to the MDF endpoint).
                Default is False.

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
        # ensure that one of `https_data_path` or `globus_data_source` have been assigned values
        if (https_data_path and globus_data_source) or \
                (https_data_path is None and globus_data_source is None):
            raise ValueError("Must assign either `https_data_path` or `globus_data_source`")

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

        # upload via HTTPS if specified
        if https_data_path:
            # gather auth'd clients necessary for publication to endpoint
            endpoint_id = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec"  # NCSA endpoint
            scope = f"https://auth.globus.org/scopes/{endpoint_id}/https"  # lets you HTTPS to specific endpoint
            pub_auths = PubAuths(
                transfer_client=self.auths["transfer"],
                auth_client_openid=AuthClient(authorizer=self.auths['openid']),
                endpoint_auth_clients={endpoint_id: AuthClient(authorizer=self.auths[scope])}
            )
            # upload (ie publish) data to endpoint
            globus_data_source = upload_to_endpoint(pub_auths, https_data_path, endpoint_id)
        # set Globus data source URL with MDF
        self.connect_client.add_data_source(globus_data_source)
        # set dataset name using the title if an abbreviated short_name isn't specified
        self.connect_client.set_source_name(kwargs.get("short_name", title))

        # do not submit to MDF if this is just a test
        if not test:
            # Globus Transfer the data from the data source to the MDF endpoint
            res = self.connect_client.submit_dataset(update=update)
        else:
            res = None
        return res

    def publish_model(self, title, creators, short_name, servable_type, serv_options, affiliations=None, paper_doi=None):
        """Simplified publishing method for servables

        Args:
            title (string): title for the servable
            creators (string | list): either the creator's name (FamilyName, GivenName) or a list of the creators' names
            short_name (string): shorthand name for the servable
            servable_type (string): the type of the servable, must be a member of ("static_method",
                                                                                   "class_method",
                                                                                   "keras",
                                                                                   "pytorch",
                                                                                   "tensorflow",
                                                                                   "sklearn")
            serv_options (dict): the servable_type specific arguments that are necessary for publishing. arguments can be found at
                                 https://dlhub-sdk.readthedocs.io/en/latest/source/dlhub_sdk.models.servables.html under the appropriate
                                 ``create_model`` signature. use the argument names as keys and their values as the values.
            affiliations (list): list of affiliations for each author
            paper_doi (str): DOI of a paper that describes the servable
        Returns:
            (string): task id of this submission, can be used to check for success
        Raises:
            ValueError: If the given servable_type is not in the list of acceptable types
            Exception: If the serv_options are incomplete or the request to publish results in an error
        """
        return self.dlhub_client.easy_publish(title, creators, short_name, servable_type, serv_options, affiliations, paper_doi)

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

    def download(self, globus: bool = True, interval: int = 20, parallel_https: int = 4, verbose: bool = False) -> 'Foundry':
        """Download a Foundry dataset

        Args:
            globus: if True, use Globus to download the data else try HTTPS
            interval: How often to wait before checking Globus transfer status
            parallel_https: Number of files to download in parallel if using HTTPS
            verbose: Produce more debug messages to screen

        Returns:
            self, for chaining
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
                # if number of missing files is greater than zero, redownload with informative message
                if len(missing_files) > 0:
                    logger.info(f"Dataset will be redownloaded, following files are missing: {missing_files}")
                else:
                    logger.info("Dataset has already been downloaded and contains all the desired files")
                    return self
            else:
                # in the case of no splits, ensure the directory contains at least one file
                if len(os.listdir(path)) >= 1:
                    logger.info("Dataset has already been downloaded and contains all the desired files")
                    return self
                else:
                    logger.info("Dataset will be redownloaded, expected file is missing")

        res = self.forge_client.search(
            f"mdf.source_id:{self.mdf['source_id']}", advanced=True
        )
        if globus:
            self.forge_client.globus_download(
                res,
                dest=self.config.local_cache_dir,
                dest_ep=self.config.destination_endpoint,
                interval=interval,
                download_datasets=True,
            )
        else:
            https_config = {
                "source_ep_id": "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec",
                "base_url": "https://data.materialsdatafacility.org",
                "folder_to_crawl": f"/foundry/{self.mdf['source_id']}/",
                "source_id": self.mdf["source_id"]
            }

            # Begin finding files to download
            task_generator = recursive_ls(self.transfer_client,
                                          https_config['source_ep_id'],
                                          https_config['folder_to_crawl'])
            with ThreadPoolExecutor(parallel_https) as executor:
                # First submit all files
                futures = [executor.submit(lambda x: download_file(x, https_config), f)
                           for f in tqdm(task_generator, disable=not verbose, desc="Finding files")]

                # Check that they completed successfully
                for result in tqdm(as_completed(futures), disable=not verbose, desc="Downloading files"):
                    if result.exception() is not None:
                        for f in futures:
                            f.cancel()
                        raise result.exception()

        # after download check making sure directory exists, contains all indicated files
        if os.path.isdir(path):
            # checking all necessary files are present
            if self.dataset.splits:
                missing_files = []
                for split in self.dataset.splits:
                    if split.path[0] == '/':  # if absolute path, make it a relative path
                        split.path = split.path[1:]
                    if not os.path.isfile(os.path.join(path, split.path)):
                        # keeping track of all files not downloaded
                        missing_files.append(split.path)
                if len(missing_files) > 0:
                    raise FileNotFoundError(f"Downloaded directory does not contain the following files: {missing_files}")

            else:
                if len(os.listdir(path)) < 1:
                    raise FileNotFoundError("Downloaded directory does not contain the expected file")
        else:
            raise NotADirectoryError("Unable to create directory to download data")

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

    def _load_data(self, file=None, source_id=None, globus=True, as_hdf5=False):
        # Build the path to access the cached data
        if source_id:
            path = os.path.join(self.config.local_cache_dir, source_id)
        else:
            path = os.path.join(self.config.local_cache_dir,
                                self.mdf["source_id"])

        # Determine which file to load, defaults to config.dataframe_file
        if not file:
            file = self.config.dataframe_file
        if path is None:
            raise ValueError(f"Path to data file is invalid; check that dataset source_id is valid: "
                             f"{source_id or self.mdf['source_id']}")
        path_to_file = os.path.join(path, file)

        # Check to see whether file exists at path
        if not os.path.isfile(path_to_file):
            raise FileNotFoundError(f"No file found at expected path: {path_to_file}")

        # Handle Foundry-defined types.
        if self.dataset.data_type.value == "tabular":
            # TODO: Add hashes and versioning to metadata and checking to the file
            read_fns = [(_read_json, {"lines": False, "path_to_file": path_to_file}),
                        (_read_json, {"lines": True, "path_to_file": path_to_file}),
                        (_read_csv, {"path_to_file": path_to_file}),
                        (_read_excel, {"path_to_file": path_to_file})]

            for fn, params in read_fns:
                try:
                    self.dataset.dataframe = fn(**params)
                except Exception as e:
                    logger.info(f"Unable to read file with {fn.__name__} with params {params}: {e}")
                if self.dataset.dataframe is not None:
                    logger.info(f"Succeeded with {fn.__name__} with params {params}")
                    break
            if self.dataset.dataframe is None:
                logger.fatal(f"Cannot read {path_to_file} as tabular data, failed to load")
                raise ValueError(f"Cannot read tabular data from {path_to_file}")

            return (
                self.dataset.dataframe[self.get_keys("input")],
                self.dataset.dataframe[self.get_keys("target")],
            )

        elif self.dataset.data_type.value == "hdf5":
            f = h5py.File(path_to_file, "r")
            special_types = ["input", "target"]
            tmp_data = {s: {} for s in special_types}
            for s in special_types:
                for key in self.get_keys(s):
                    if as_hdf5:
                        tmp_data[s][key] = f[key]
                    elif isinstance(f[key], h5py.Group):
                        if is_pandas_pytable(f[key]):
                            df = pd.read_hdf(path_to_file, key)
                            tmp_data[s][key] = df
                        else:
                            tmp_data[s][key] = f[key]
                    elif isinstance(f[key], h5py.Dataset):
                        tmp_data[s][key] = f[key][0:]
            return tmp_data
        else:
            raise NotImplementedError

    def _get_inputs_targets(self, split: str = None):
        """Get Inputs and Outputs from a Foundry Dataset

        Arguments:
            split (string): Split to get inputs and outputs from.
                    **Default:** ``None``

        Returns: (Tuple) Tuple of the inputs and outputs
        """
        raw = self.load_data(as_hdf5=False)

        if not split:
            split = self.dataset.splits[0].type

        if self.dataset.data_type.value == "hdf5":
            inputs = []
            targets = []
            for key in self.dataset.keys:
                if len(raw[split][key.type][key.key[0]].keys()) != self.dataset.n_items:
                    continue

                # Get a numpy array of all the values for each item for that key
                val = np.array([raw[split][key.type][key.key[0]][k] for k in raw[split][key.type][key.key[0]].keys()])
                if key.type == 'input':
                    inputs.append(val)
                else:
                    targets.append(val)

            return (inputs, targets)

        elif self.dataset.data_type.value == "tabular":
            inputs = []
            targets = []

            for index, arr in enumerate([inputs, targets]):
                df = raw[split][index]
                for key in df.keys():
                    arr.append(df[key].values)

            return (inputs, targets)

        else:
            raise NotImplementedError

    def to_torch(self, split: str = None):
        """Convert Foundry Dataset to a PyTorch Dataset

        Arguments:
            split (string): Split to create PyTorch Dataset on.
                    **Default:** ``None``

        Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split

        """
        from foundry.loaders.torch_wrapper import TorchDataset

        inputs, targets = self._get_inputs_targets(split)
        return TorchDataset(inputs, targets)

    def to_tensorflow(self, split: str = None):
        """Convert Foundry Dataset to a Tensorflow Sequence

        Arguments:
            split (string): Split to create Tensorflow Sequence on.
                    **Default:** ``None``

        Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split

        """
        from foundry.loaders.tf_wrapper import TensorflowSequence

        inputs, targets = self._get_inputs_targets(split)
        return TensorflowSequence(inputs, targets)
