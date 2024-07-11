from pathlib import Path
import pytest
import os

from mdf_connect_client import MDFConnectClient
from mdf_forge import Forge
import mdf_toolbox
import pandas as pd

from foundry import foundry

is_gha = os.getenv("GITHUB_ACTIONS")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


@pytest.fixture
def auths():
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

    if is_gha:
        auths = mdf_toolbox.confidential_login(client_id=client_id,
                                               client_secret=client_secret,
                                               services=services, make_clients=True)

        search_auth = mdf_toolbox.confidential_login(client_id=client_id,
                                                     client_secret=client_secret,
                                                     services=["search"], make_clients=False)
    else:
        auths = mdf_toolbox.login(services=services, make_clients=True)
        search_auth = mdf_toolbox.login(services=["search"], make_clients=False)

    auths['search_authorizer'] = search_auth['search']

    yield auths


@pytest.fixture()
def testing_data_dir():
    return str(Path(__file__).parent) + '/test_data'


@pytest.fixture
def elwood_data():
    test_dataset_name = "elwood_md_v1.2"
    test_doi = "10.18126/8p6m-e135"
    expected_title = "Project Elwood: MD Simulated Monomer Properties"
    yield test_dataset_name, test_doi, expected_title


@pytest.fixture
def iris_data():
    pub_test_dataset = "_test_foundry_iris_dev_v2.1"
    pub_expected_title = "Iris Dataset"
    yield pub_test_dataset, pub_expected_title


# FoundryCache testing

def test_loading_as_dict(auths, elwood_data, testing_data_dir):
    # test loading the dataset from a local (static) copy
    test_dataset_name, test_doi, expected_title = elwood_data

    f = foundry.Foundry(authorizers=auths, local_cache_dir=testing_data_dir)
    search_results = f.search(test_dataset_name, as_list=True)
    elwood_data = search_results[0].get_as_dict()
    X, y = elwood_data['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)


def test_foundry_init(auths, elwood_data):
    test_dataset_name, test_doi, expected_title = elwood_data

    f = foundry.Foundry(authorizers=auths)
    assert isinstance(f.forge_client, Forge)
    assert isinstance(f.connect_client, MDFConnectClient)

def test_search(auths, elwood_data):
    test_dataset_name, test_doi, expected_title = elwood_data

    f = foundry.Foundry(authorizers=auths)
    q = "Elwood"
    ds = f.search(q)

    assert isinstance(ds, pd.DataFrame)
    assert len(ds) > 0

    dataset = ds.iloc[0].FoundryDataset

    # assert ds.iloc[0]['name'] is not None
    assert dataset.dc.titles[0].title == expected_title

    # assert ds.iloc[0]['source_id'] is not None
    assert dataset.dataset_name == test_dataset_name

    # assert ds.iloc[0]['year'] is not None
    assert dataset.dc.publicationYear is not None


def test_search_as_list(auths, elwood_data):
    auths = auths
    test_dataset_name, test_doi, expected_title = elwood_data

    f = foundry.Foundry(authorizers=auths)
    q = "Elwood"
    ds = f.search(q, as_list=True)

    assert isinstance(ds, list)
    assert len(ds) > 0

    dataset = ds[0]

    # assert ds.iloc[0]['name'] is not None
    assert dataset.dc.titles[0].title == expected_title

    # assert ds.iloc[0]['source_id'] is not None
    assert dataset.dataset_name == test_dataset_name

    # assert ds.iloc[0]['year'] is not None
    assert dataset.dc.publicationYear is not None


def test_search_limit(auths, elwood_data):
    f = foundry.Foundry(authorizers=auths)
    ds = f.search(limit=10)

    assert isinstance(ds, pd.DataFrame)
    assert len(ds) == 10


@pytest.mark.skipif(bool(is_gha), reason="pytest.raises seems to cause issues in GHA?")
def test_search_no_results():
    f = foundry.Foundry()

    with pytest.raises(Exception) as exc_info:
        f.search('chewbacca')

    err = exc_info.value
    assert hasattr(err, '__cause__')
