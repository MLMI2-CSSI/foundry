import mdf_toolbox
import pandas as pd
from typing import Any, Dict, List, ClassVar, Optional
import logging
from pydantic import Field, ConfigDict

from mdf_connect_client import MDFConnectClient
from mdf_forge import Forge
from globus_sdk import AuthClient

from .auth import PubAuths
from .foundry_cache import FoundryCache
from .foundry_dataset import FoundryDataset
from .https_upload import upload_to_endpoint
from .utils import is_doi

from foundry.models import FoundryBase

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)


class HiddenColumnDataFrame(pd.DataFrame):
    """
    A subclass of pd.DataFrame that supports hiding a specific column. This is
    intended to mimic display of search results from an earlier version while
    providing access to associated FoundryDataset objects for each entry in the
    dataframe via the `get_dataset_by_[name/doi]()` function.

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
        forge_client (Any): The Forge client.
        connect_client (Any): The MDF Connect client.
        transfer_client (Any): The Globus transfer client.
        auth_client (Any): The authentication client.
        index (str): The index to use for search and data publication.
        auths (Any): The authorizers used for authentication.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    forge_client: Any = Field(default=None)
    connect_client: Any = Field(default=None)
    transfer_client: Any = Field(default=None)
    auth_client: Any = Field(default=None)
    index: str = Field(default="")
    auths: Any = Field(default=None)

    use_globus: bool = Field(default=True)
    verbose: bool = Field(default=False)
    interval: int = Field(default=10)
    parallel_https: int = Field(default=4)
    local_cache_dir: Optional[str] = Field(default=None)

    foundry_cache: FoundryCache = Field(default=None, exclude=True)

    DOI: ClassVar[str] = 'mdf.landing_page'
    title: ClassVar[str] = 'dc.titles.title'
    organization: ClassVar[str] = "Foundry"

    def __init__(self,
                 no_browser: bool = False,
                 no_local_server: bool = False,
                 index: str = "mdf",
                 authorizers: dict = None,
                 use_globus: bool = True,
                 verbose: bool = False,
                 interval: int = 10,
                 parallel_https: int = 4,
                 local_cache_dir: str = None,
                 **data):
        """Initialize a Foundry client"""
        super().__init__(**data)
        self.index = index
        self.use_globus = use_globus
        self.verbose = verbose
        self.interval = interval
        self.parallel_https = parallel_https
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

        self.use_globus = use_globus
        self.interval = interval
        self.parallel_https = parallel_https
        self.verbose = verbose
        local_cache_dir

        self.foundry_cache = FoundryCache(self.forge_client,
                                          self.transfer_client,
                                          use_globus,
                                          interval,
                                          parallel_https,
                                          verbose,
                                          local_cache_dir)

    def search(self, query: str = None, limit: int = None, as_list: bool = False) -> List[FoundryDataset]:
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
            foundry_schema = metadata['projects']['foundry']
            dc = metadata['dc']
            name = metadata['mdf']['source_id']

            ds = FoundryDataset(**{'dataset_name': name,
                                   'datacite_entry': dc,
                                   'foundry_schema': foundry_schema,
                                   'foundry_cache': self.foundry_cache})

            return ds

        except Exception as e:
            logger.error(f"The mdf entry {metadata['mdf']['source_id']} is missing a {e} section - cannot generate a foundry dataset object")

    def get_dataset(self, doi: str) -> FoundryDataset:
        """Get exactly one dataset by DOI

        Should only return a single result.

        Args:
            doi (str): doi of desired dataset

        Returns:
             (FoundryDataset): A FoundryDataset loaded from the dataset metadata
        """
        logger.info('using DOI to retrieve metadata')
        forge = self.forge_client.match_resource_types("dataset")
        results = forge.match_dois(doi).search()
        if len(results) < 1:
            return None
        else:
            return self.dataset_from_metadata(results[0])

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
                                          'title': result.dc.titles[0].title,
                                          'year': result.dc.publicationYear,
                                          'DOI': result.dc.identifier.identifier.root,
                                          'FoundryDataset': result}))
        df = HiddenColumnDataFrame(series_list, hidden_column='FoundryDataset')
        return df

    def publish_dataset(self,
                        foundry_dataset: FoundryDataset,
                        update: bool = False,
                        test: bool = False):
        """Submit a dataset for publication; can choose to submit via HTTPS using `local_data_path` or via Globus
            Transfer using the `globus_data_source` argument. Only one upload method may be specified.
        Args:
            foundry_dataset (FoundryDataset): The dataset to be published.
            update (bool): True if this is an update to a prior data package.
            test (bool): If True, do not submit the dataset for publication (ie transfer to the MDF endpoint).
                Default is False.

        Returns:
            dict: MDF Connect Response. Response from MDF Connect to allow tracking
            of dataset. Contains `source_id`, which can be used to check the
            status of the submission.
        """

        # ensure that one of `local_data_path` or `globus_data_source` have been assigned values
        if (not hasattr(foundry_dataset, '_local_data_path') and not hasattr(foundry_dataset, '_globus_data_source')):
            raise ValueError("Must add data to your FoundryDataset object (use the FoundryDataset.add_data() method) before publishing")
        if (hasattr(foundry_dataset, '_local_data_path') and hasattr(foundry_dataset, '_globus_data_source')):
            raise ValueError("Dataset cannot contain both `local_data_path` and `globus_data_source` attributes. "
                             "Choose one by adding via the FoundryDataset.add() method.")
        if (hasattr(foundry_dataset, '_local_data_path') and
            foundry_dataset._local_data_path is None) or \
           (hasattr(foundry_dataset, '_globus_data_source') and foundry_dataset._globus_data_source is None):
            raise ValueError("Must assign a value to `local_data_path` OR `globus_data_source` in your FoundryDataset object - "
                             "use the FoundryDataset.add_data() method (cannot be None)")

        self.connect_client.dc = foundry_dataset.clean_dc_dict()
        self.connect_client.set_organization(self.organization)
        self.connect_client.set_project_block("foundry", foundry_dataset)

        # upload via HTTPS if specified
        if foundry_dataset._local_data_path:
            # gather auth'd clients necessary for publication to endpoint
            endpoint_id = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec"  # NCSA endpoint
            scope = f"https://auth.globus.org/scopes/{endpoint_id}/https"  # lets you HTTPS to specific endpoint
            pub_auths = PubAuths(
                transfer_client=self.auths["transfer"],
                auth_client_openid=AuthClient(authorizer=self.auths['openid']),
                endpoint_auth_clients={endpoint_id: AuthClient(authorizer=self.auths[scope])}
            )
            # upload (ie publish) data to endpoint
            globus_data_source = upload_to_endpoint(pub_auths, foundry_dataset._local_data_path, endpoint_id)
        else:
            # set Globus data source URL with MDF
            globus_data_source = foundry_dataset._globus_data_source
        # set Globus data source URL with MDF
        self.connect_client.add_data_source(globus_data_source)
        self.connect_client.set_source_name(foundry_dataset.dataset_name)

        # do not submit to MDF if this is just a test
        if not test:
            # Globus Transfer the data from the data source to the MDF endpoint
            res = self.connect_client.submit_dataset(update=update)
        else:
            res = None
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
