import pytest
from unittest.mock import MagicMock

@pytest.fixture(scope="session")
def mock_authorizers():
    """
    Provides a mock 'auths' dictionary similar to what mdf_toolbox.login returns.
    This allows testing Foundry without actual Globus authentication.
    The mock objects are very basic and may need to be enhanced if specific
    methods or attributes of the authorizers/clients are accessed in tests.
    """
    mock_auths = {
        "data_mdf": MagicMock(),
        "mdf_connect": MagicMock(),
        "search": MagicMock(),  # This would be a SearchClient instance
        "petrel": MagicMock(),
        "transfer": MagicMock(),  # This would be a TransferClient instance
        "openid": MagicMock(),  # This would be an AuthClient instance for OpenID
        "funcx": MagicMock(), # Deprecated, but kept for compatibility if still in services list
        "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all": MagicMock(), # funcx
        "https://auth.globus.org/scopes/f10a69a9-338c-4e5b-baa1-0dc92359ab47/https": MagicMock(), # Eagle HTTPS
        "https://auth.globus.org/scopes/82f1b5c6-6e9b-11e5-ba47-22000b92c6ec/https": MagicMock(), # NCSA HTTPS
        "https://auth.globus.org/scopes/d31d4f5d-be37-4adc-a761-2f716b7af105/action_all": MagicMock(), # Globus Search Lambda
        "search_authorizer": MagicMock() # Specific search authorizer
    }

    # If clients have an 'authorizer' attribute that is used, mock it too.
    # For example, if some_client.authorizer.is_logged_in is called:
    for key in mock_auths:
        if hasattr(mock_auths[key], 'authorizer'):
            mock_auths[key].authorizer = MagicMock()
        
    # Specific mock for AuthClient used in publish_dataset for PubAuths
    # It needs to be an instance that can be passed to AuthClient() constructor
    mock_auths['openid_authorizer_for_auth_client'] = MagicMock()
    
    # Mock for the NCSA HTTPS endpoint authorizer specifically
    ncsa_https_scope = "https://auth.globus.org/scopes/82f1b5c6-6e9b-11e5-ba47-22000b92c6ec/https"
    mock_auths[ncsa_https_scope] = MagicMock()


    # Mock the `AuthClient` that would be initialized with `auths['openid']`
    # This is used in `f.auth_client = AuthClient(authorizer=self.auths['openid'])`
    # and in `PubAuths(auth_client_openid=AuthClient(authorizer=self.auths['openid']))`
    # We need to ensure that when AuthClient is called with our mock openid authorizer,
    # it returns a usable mock AuthClient.
    # This is tricky to do globally here, might be better to patch AuthClient constructor.

    return mock_auths

@pytest.fixture
def mock_foundry(mock_authorizers, mocker):
    """
    Provides a Foundry instance initialized with mock authorizers.
    Also mocks mdf_toolbox.login to prevent actual authentication calls.
    """
    mocker.patch("mdf_toolbox.login", return_value=mock_authorizers)
    mocker.patch("mdf_toolbox.confidential_login", return_value=mock_authorizers)
    
    # Mock the AuthClient constructor to return a MagicMock instance
    # This will affect AuthClient(authorizer=self.auths['openid']) and
    # AuthClient(authorizer=self.auths[scope]) in publish_dataset
    mock_auth_client_instance = MagicMock()
    mocker.patch("globus_sdk.AuthClient", return_value=mock_auth_client_instance)

    from foundry import Foundry
    # We pass index="mdf" as it's a common default.
    # Tests requiring a different index can initialize their own Foundry instance
    # or this fixture can be parameterized.
    return Foundry(authorizers=mock_authorizers, index="mdf")

@pytest.fixture
def mock_foundry_dataset(mock_foundry, sample_metadata):
    """
    Provides a mock FoundryDataset instance.
    It uses a Foundry instance that has auth mocked.
    The dataset is initialized with sample metadata.
    """
    from foundry.foundry_dataset import FoundryDataset
    from foundry.foundry_cache import FoundryCache
    from foundry.models import FoundryDatacite, FoundrySchema
    
    # Create a mock FoundryCache instance
    mock_cache = MagicMock(spec=FoundryCache)

    # Prepare datacite_entry and foundry_schema from sample_metadata
    # This assumes sample_metadata includes 'dc' and 'projects.foundry' keys
    # similar to what dataset_from_metadata would process.
    datacite_entry_data = sample_metadata.get('dc', {})
    foundry_schema_data = sample_metadata.get('projects', {}).get('foundry', {})
    dataset_name = sample_metadata.get('mdf', {}).get('source_id', 'test_dataset')

    # Ensure essential fields are present for FoundryDatacite and FoundrySchema
    # For simplicity, using basic valid structures. Tests needing specific metadata
    # details should construct their FoundryDataset instances directly.
    if not datacite_entry_data.get('titles'):
        datacite_entry_data['titles'] = [{'title': 'Test Title'}]
    if not datacite_entry_data.get('creators'):
        datacite_entry_data['creators'] = [{'creatorName': 'Test Creator'}]
    if not datacite_entry_data.get('publisher'):
        datacite_entry_data['publisher'] = 'Test Publisher'
    if not datacite_entry_data.get('publicationYear'):
        datacite_entry_data['publicationYear'] = '2023'
    if not datacite_entry_data.get('identifier'):
        datacite_entry_data['identifier'] = {'identifier': '10.1234/test', 'identifierType': 'DOI'}

    # Minimal foundry_schema
    if not foundry_schema_data.get('splits'): # Assuming FoundrySchema expects splits
        foundry_schema_data['splits'] = []


    datacite_entry = FoundryDatacite(**datacite_entry_data)
    foundry_schema = FoundrySchema(**foundry_schema_data)

    dataset = FoundryDataset(dataset_name=dataset_name,
                             datacite_entry=datacite_entry,
                             foundry_schema=foundry_schema,
                             foundry_cache=mock_cache)
    return dataset

@pytest.fixture(scope="session")
def sample_metadata():
    """
    Provides a sample metadata dictionary, mimicking a result from Forge.
    """
    return {
        "mdf": {
            "source_id": "test_dataset_v1.0",
            "ingest_date": "2023-01-01T00:00:00Z",
        },
        "dc": {
            "titles": [{"title": "Sample Test Dataset"}],
            "creators": [{"creatorName": "Test Author"}],
            "publisher": "Test Publisher",
            "publicationYear": "2023",
            "subjects": [{"subject": "testing"}, {"subject": "mocking"}],
            "identifier": {
                "identifier": "10.1234/mock.dataset",
                "identifierType": "DOI"
            },
            "descriptions": [{"description": "A dataset for testing purposes."}]
        },
        "projects": {
            "foundry": {
                "splits": [
                    {"label": "train", "path": "train/", "type": "tabular"},
                    {"label": "test", "path": "test/", "type": "tabular"}
                ],
                "data_type": "tabular",
                "task_type": "classification",
                "inputs": ["feature1", "feature2"],
                "outputs": ["label"],
                "output_details": [{"name": "label", "type": "categorical", "classes": ["A", "B"]}]
            }
        }
    }
@pytest.fixture(scope="session")
def sample_search_results(sample_metadata):
    """
    Provides a list containing a single sample metadata dictionary.
    This mimics the direct output of Forge().search()
    """
    return [sample_metadata]

@pytest.fixture(scope="session")
def sample_doi_search_result(sample_metadata):
    """
    Provides a list containing a single sample metadata dictionary,
    mimicking the direct output of Forge().match_dois().search()
    """
    return [sample_metadata]

@pytest.fixture(scope="session")
def sample_foundry_dataset_search_result(sample_metadata):
    """
    Provides a Pandas DataFrame mimicking the output of Foundry.search()
    when as_list=False.
    This requires creating a mock FoundryDataset object.
    """
    import pandas as pd
    from foundry.foundry_dataset import FoundryDataset
    from foundry.models import FoundryDatacite, FoundrySchema

    # Simplified FoundryDataset for this fixture
    # In real tests, mock_foundry_dataset fixture might be more appropriate
    # if complex interactions with the dataset object are needed.

    datacite_entry = FoundryDatacite(**sample_metadata['dc'])
    foundry_schema = FoundrySchema(**sample_metadata['projects']['foundry'])
    mock_cache = MagicMock()

    dataset = FoundryDataset(dataset_name=sample_metadata['mdf']['source_id'],
                             datacite_entry=datacite_entry,
                             foundry_schema=foundry_schema,
                             foundry_cache=mock_cache) # type: ignore

    # Using the HiddenColumnDataFrame structure
    from foundry.foundry import HiddenColumnDataFrame
    data = [{
        'dataset_name': dataset.dataset_name,
        'title': dataset.dc.titles[0].title,
        'year': dataset.dc.publicationYear,
        'DOI': dataset.dc.identifier.identifier.root, # Corrected access
        'FoundryDataset': dataset
    }]
    df = HiddenColumnDataFrame(data, hidden_column='FoundryDataset')
    return df
