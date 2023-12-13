import mdf_toolbox
import pandas as pd
from typing import Any, Dict, List
import logging

from mdf_connect_client import MDFConnectClient
from mdf_forge import Forge
from dlhub_sdk import DLHubClient
from globus_sdk import AuthClient

from .auth import PubAuths
from .utils import is_doi

from foundry.models import (
    FoundrySchema,
    FoundryBase
)

from foundry.foundry_dataset import FoundryDataset

# from foundry import FOUNDRY_CACHE
# from foundry.foundry_cache import FoundryCache

from foundry.https_upload import upload_to_endpoint

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)


class HiddenColumnDataFrame(pd.DataFrame):
    """
    A subclass of pd.DataFrame that supports hiding a specific column.

    Parameters:
    *args: positional arguments
        Positional arguments passed to the parent class constructor.
    hidden_column: str, optional
        The name of the column to be hidden.
    **kwargs: keyword arguments
        Keyword arguments passed to the parent class constructor.

    Attributes:
    hidden_column: str or None
        The name of the hidden column.

    Methods:
    _repr_html_():
        Overrides the _repr_html_ method of the parent class to hide the specified column in the HTML representation.
    get_dataset_by_name(dataset_name):
        Returns the FoundryDataset associated with the given dataset name. Can also handle a DOI.
    get_dataset_by_doi(doi):
        Returns the FoundryDataset associated with the given DOI.

    """

    def __init__(self, *args, hidden_column=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.hidden_column = hidden_column

    def _repr_html_(self):
        if self.hidden_column is not None and self.hidden_column in self.columns:
            return self.drop(self.hidden_column, axis=1)._repr_html_()

    def get_dataset_by_name(self, dataset_name):
        if is_doi(dataset_name):
            return self.get_dataset_by_doi(dataset_name)
        else:
            return self[self.dataset_name == dataset_name]['FoundryDataset'].iloc[0]

    def get_dataset_by_doi(self, doi):
        return self[self.DOI == doi]['FoundryDataset'].iloc[0]


class Foundry(FoundryBase):
    """Foundry Client Base Class

    This class represents a client for interacting with the Foundry service. It provides methods for searching and
    accessing datasets, as well as publishing new datasets.

    Attributes:
        dlhub_client (Any): The DLHub client.
        forge_client (Any): The Forge client.
        connect_client (Any): The MDF Connect client.
        transfer_client (Any): The Globus transfer client.
        auth_client (Any): The authentication client.
        index (str): The index to use for search and data publication.
        auths (Any): The authorizers used for authentication.

    """

    dlhub_client: Any
    forge_client: Any
    connect_client: Any
    transfer_client: Any
    auth_client: Any
    index = ""
    auths: Any

    def __init__(self,
                 no_browser: bool = False,
                 no_local_server: bool = False,
                 index:str = "mdf",
                 authorizers: dict = None,
                 use_globus: bool = True,
                 verbose: bool = False,
                 interval: int = 10,
                 local_cache_dir: str = None,
                 **data):
        """Initialize a Foundry client

        Args:
            no_browser (bool): Whether to open the browser for the Globus Auth URL.
            no_local_server (bool): Whether a local server is available. This should be `False` when on a remote server (e.g., Google Colab).
            index (str): Index to use for search and data publication. Choices are `mdf` or `mdf-test`.
            authorizers (dict): A dictionary of authorizers to use, following the `mdf_toolbox` format.
            use_globus (bool): If True, download using Globus, otherwise use HTTPS.
            verbose (bool): If True, print additional debug information.
            interval (int): How often to poll Globus to check if transfers are complete.
            local_cache_dir (str): Optional location to store downloaded data - if not specified, defaults to either environmental variable ('FOUNDRY_LOCAL_CACHE_DIR') or './data'
            data (dict): Other arguments, e.g., results from an MDF search result that are used to populate Foundry metadata fields.

        Returns:
            An initialized and authenticated Foundry client.
        """
        super().__init__(**data)
        self.index = index
        self.auths = None
        self.use_globus = use_globus
        self.verbose = verbose
        self.interval = interval
        if local_cache_dir:
            self.local_cache_dir = local_cache_dir

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

    def search(self, query: str = None, limit: int = None, as_list: bool = False) -> [FoundryDataset]:
        """Search available Foundry datasets

        This method searches for available Foundry datasets based on the provided query string.
        If a DOI is provided as the query, it retrieves the metadata for that specific dataset.
        If a query string is provided, it retrieves the metadata for datasets that match the query.
        The limit parameter can be used to specify the maximum number of results to return.

        Args:
            query (str): The query string to match. If a DOI is provided, it retrieves the metadata for that specific dataset.
            limit (int): The maximum number of results to return.
            as_list (bool): If True, the search results will be returned as a list instead of a DataFrame.

        Returns:
            List[FoundryDataset] or DataFrame: A list of search results as FoundryDataset objects or a DataFrame if as_list is False.

        Raises:
            Exception: If no results are found for the provided query.

        Example:
            >>> foundry = Foundry()
            >>> results = foundry.search(query="materials science", limit=10)
            >>> print(len(results))
            10
        """
        if (query is not None) and (is_doi(query)):
            metadata_list = [self.get_metadata_by_doi(query)]
        else:
            metadata_list = self.get_metadata_by_query(query, limit)

        if len(metadata_list) == 0:
            raise Exception(f"load: No results found for the query '{query}'")

        foundry_datasets = []
        for metadata in metadata_list:
            ds = self.dataset_from_metadata(metadata)
            if ds:
                foundry_datasets.append(ds)

        logger.info(f"Search for '{query}' returned {len(foundry_datasets)} foundry datasets out of {len(metadata_list)} matches")

        if as_list:
            return foundry_datasets

        foundry_datasets = self.search_results_to_dataframe(foundry_datasets)

        return foundry_datasets

    def list(self, limit: int = None):
        """List available Foundry datasets

        Args:
            limit (int): maximum number of results to return

        Returns:
            List[FoundryDataset]: List of FoundryDataset objects
        """
        return self.search(limit=limit)

    def dataset_from_metadata(self, metadata: dict) -> FoundryDataset:
        """ Converts the result of a forge query to a FoundryDatset object

        Args:
            metadata (dict): result from a forge query

        Returns:
            FoundryDataset: a FoundryDataset object created from the metadata

        Raises:
            Exception: If the mdf entry is missing a section, cannot generate a foundry dataset object
        """
        try:
            foundry_schema = FoundrySchema(**metadata['projects']['foundry'])
            dc = metadata['dc']
            name = metadata['mdf']['source_id']

            ds = FoundryDataset(**{'dataset_name': name,
                                   'foundry_schema': foundry_schema,
                                   'transfer_client': self.auths["transfer"],
                                   'datacite_entry': dc,
                                   'use_globus': self.use_globus,
                                   'interval': self.interval,
                                   'verbose': self.verbose,
                                   'forge_client': self.forge_client,
                                   'local_cache_dir': self.local_cache_dir})

            return ds

        except Exception as e:
            logger.error(f"The mdf entry {metadata['mdf']['source_id']} is missing a {e} section - cannot generate a foundry dataset object")

    def get_dataset_by_name(self, name: str) -> FoundryDataset:
        """Query foundry datasets by name

        This method queries the foundry datasets by name, where the name is equivalent to the 'source_id' in MDF.
        It should only return a single result.

        Args:
            name (str): The name (source_id) of the desired dataset.

        Returns:
            FoundryDataset: A FoundryDataset object representing the result of the query.
        """

        forge = self.forge_client.match_field(
                    "mdf.organizations", self.organization
                    ).match_resource_types("dataset")
        metadata = forge.match_field("mdf.source_id", name).search()[0]
        ds = self.dataset_from_metadata(metadata)
        return ds

    def get_metadata_by_doi(self, doi: str) -> dict:
        """Query foundry datasets by DOI

        Should only return a single result.

        Args:
            doi (str): doi of desired dataset

        Returns:
            metadata (dict): result from a forge query
        """
        logger.info('using DOI to retrieve metadata')
        forge = self.forge_client.match_resource_types("dataset")
        results = forge.match_dois(doi).search()
        if len(results) < 1:
            return None
        else:
            return results[0]

    def get_metadata_by_query(self, q: str, limit: int) -> dict:
        """Submit query to forge client and return results

        Args:
            q (str): query string
                The query string to be submitted to the forge client.
            limit (int): maximum number of results to return
                The maximum number of results to be returned by the foundry client.

        Returns:
            metadata (dict): result from a forge query
                The result from the forge query, represented as a dictionary.
        """

        forge = self.forge_client.match_resource_types("dataset").match_organizations('foundry')
        metadata = forge.search(advanced=True)
        if q:
            metadata = self.filter_datasets_by_query(q, metadata)
        if limit:
            metadata = metadata[:limit]
        return metadata

    def filter_datasets_by_query(self, query_string: str, metadata: List[Dict]) -> List[Dict]:
        """
        Filters the given metadata based on the provided query string.

        Args:
            query_string (str): The query string to filter the metadata.
            metadata (list): The list of metadata to be filtered.

        Returns:
            list[dict]: A list of dicts that match the query string.
        """
        matches = []
        for md in metadata:
            if str(md).lower().find(query_string.lower()) != -1:
                matches.append(md)
        return matches

    def search_results_to_dataframe(self, results):
        """
        Convert a list of results into a pandas DataFrame.

        Args:
            results (list): A list of results.

        Returns:
            DataFrame: A pandas DataFrame containing the converted results.
        """
        series_list = []
        for result in results:
            series_list.append(pd.Series({'dataset_name': result.dataset_name,
                                          'title': result.dc['titles'][0]['title'],
                                          'year': result.dc['publicationYear'],
                                          'DOI': result.dc['identifier']['identifier'],
                                          'FoundryDataset': result}))
        df = HiddenColumnDataFrame(series_list, hidden_column='FoundryDataset')
        return df

    def publish_dataset(self,
                        foundry_metadata: Dict[str, Any],
                        title: str, authors: List[str],
                        https_data_path: str = None,
                        globus_data_source: str = None,
                        update: bool = False,
                        publication_year: int = None,
                        test: bool = False,
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
        # ensure metadata is properly formatted
        self.validate_metadata(foundry_metadata)

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
        self.connect_client.add_organization(self.organization)
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
