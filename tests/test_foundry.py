import os
import shutil
import pytest
from datetime import datetime
import mdf_toolbox
import pandas as pd
from mdf_forge import Forge
from foundry import Foundry
from dlhub_sdk import DLHubClient
from mdf_connect_client import MDFConnectClient

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
is_gha = os.getenv("GITHUB_ACTIONS")

services = [
            "data_mdf",
            "mdf_connect",
            "search",
            "dlhub",
            "petrel",
            "transfer",
            "openid",
            "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all"]

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

# updated test dataset for publication
pub_test_dataset = "_test_foundry_iris_dev_v2.1"
pub_expected_title = "Iris Dataset"

# test dataset for all other tests
test_dataset = "foundry_experimental_band_gaps_v1.1"
expected_title = "Graph Network Based Deep Learning of Band Gaps - Experimental Band Gaps"


# Kept the Old metadata format in case we ever want to refer back
old_test_metadata = {
    "inputs": ["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"],
    "input_descriptions": ["sepal length in unit(cm)", "sepal width in unit(cm)", "petal length in unit(cm)",
                           "petal width in unit(cm)"],
    "input_units": ["cm", "cm", "cm", "cm"],
    "outputs": ["y"],
    "output_descriptions": ["flower type"],
    "output_units": [],
    "output_labels": ["setosa", "versicolor", "virginica"],
    "short_name": "iris_example",
    "package_type": "tabular"
}


pub_test_metadata = {
    "keys":[
        {
            "key": ["sepal length (cm)"],
            "type": "input",
            "units": "cm",
            "description": "sepal length in unit(cm)"
        },
        {
            "key": ["sepal width (cm)"],
            "type": "input",
            "units": "cm",
            "description": "sepal width in unit(cm)"
        },
        {
            "key": ["petal length (cm)"],
            "type": "input",
            "units": "cm",
            "description": "petal length in unit(cm)"
        },
        {
            "key": ["petal width (cm)"],
            "type": "input",
            "units": "cm",
            "description": "petal width in unit(cm)"
        },
        {
            "key": ["y"],
            "type": "output",
            "units": "",
            "description": "flower type",
            "classes": [
                {
                    "label": "0",
                    "name": "setosa"
                },
                {
                    "label": "1",
                    "name": "versicolor"
                },
                {
                    "label": "2",
                    "name": "virginica"
                }
            ]
        }
    ],
    'splits': [
        {'label': 'train', 'path': 'train.json', 'type': 'train'},
        {'label': 'test', 'path': 'test.json', 'type': 'test'}
    ],
    "short_name": "example_AS_iris_test_{:.0f}".format(datetime.now().timestamp()),
    "data_type": "tabular",
    'task_type': ['unsupervised', 'generative'],
    'domain': ['materials science', 'chemistry'],
    'n_items': 1000
}

# Globus endpoint for '_iris_dev' for test publication
pub_test_data_source = "https://app.globus.org/file-manager?origin_id=e38ee745-6d04-11e5-ba46-22000b92c6ec&origin_path=%2Ffoundry-test%2Firis-dev%2F"


# Quick function to delete any downloaded test data
def _delete_test_data(foundry_obj):
    path = os.path.join(foundry_obj.config.local_cache_dir, test_dataset)
    if os.path.isdir(path):
        shutil.rmtree(path)


def test_foundry_init():
    f = Foundry(authorizers=auths)
    assert isinstance(f.forge_client, Forge)
    assert isinstance(f.connect_client, MDFConnectClient)

    if not is_gha:
        assert isinstance(f.dlhub_client, DLHubClient)

        f2 = Foundry(authorizers=auths, no_browser=False, no_local_server=True)
        assert isinstance(f2.dlhub_client, DLHubClient)
        assert isinstance(f2.forge_client, Forge)
        assert isinstance(f2.connect_client, MDFConnectClient)

        f3 = Foundry(authorizers=auths, no_browser=True, no_local_server=False)
        assert isinstance(f3.dlhub_client, DLHubClient)
        assert isinstance(f3.forge_client, Forge)
        assert isinstance(f3.connect_client, MDFConnectClient)


def test_list():
    f = Foundry(authorizers=auths)
    ds = f.list()
    assert isinstance(ds, pd.DataFrame)
    assert len(ds) > 0


def test_metadata_pull():
    f = Foundry(authorizers=auths)
    assert f.dc == {}
    f = f.load(test_dataset, download=False, authorizers=auths)
    assert f.dc["titles"][0]["title"] == expected_title


def test_download_https():
    f = Foundry(authorizers=auths)
    _delete_test_data(f)

    f = f.load(test_dataset, download=True, globus=False, authorizers=auths)
    assert f.dc["titles"][0]["title"] == expected_title
    _delete_test_data(f)


def test_dataframe_load():
    f = Foundry(authorizers=auths)
    _delete_test_data(f)

    f = f.load(test_dataset, download=True, globus=False, authorizers=auths)
    res = f.load_data()
    X, y = res['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)
    _delete_test_data(f)


@pytest.mark.skipif(bool(is_gha), reason="Test does not succeed online")  # PLEASE CONFIRM THIS BEHAVIOR IS INTENDED
def test_download_globus():
    f = Foundry(authorizers=auths, no_browser=True, no_local_server=True)
    _delete_test_data(f)

    f = f .load(test_dataset, download=True)
    assert f.dc["titles"][0]["title"] == expected_title
    _delete_test_data(f)


@pytest.mark.skipif(bool(is_gha), reason="Test does not succeed online")  # PLEASE CONFIRM THIS BEHAVIOR IS INTENDED
def test_globus_dataframe_load():
    f = Foundry(authorizers=auths, no_browser=True, no_local_server=True)
    _delete_test_data(f)

    f = f.load(test_dataset, download=True)
    res = f.load_data()
    X, y = res['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)
    _delete_test_data(f)


@pytest.mark.skipif(bool(is_gha), reason="Test does not succeed online")  # PLEASE CONFIRM THIS BEHAVIOR IS INTENDED
def test_publish():
    # TODO: automate dealing with curation and cleaning after tests

    f = Foundry(authorizers=auths, index="mdf-test", no_browser=True, no_local_server=True)

    timestamp = datetime.now().timestamp()
    title = "scourtas_example_iris_test_publish_{:.0f}".format(timestamp)
    short_name = "example_AS_iris_test_{:.0f}".format(timestamp)
    authors = ["A Scourtas"]

    res = f.publish(pub_test_metadata, pub_test_data_source, title, authors, short_name=short_name)

    # publish with short name
    assert res['success']
    assert res['source_id'] == "_test_example_iris_{:.0f}_v1.1".format(timestamp)

    # TODO: publish with long title -- for some reason even when I change the title, it still says it's already pub'd
    # title += "long"
    # res = f.publish(pub_test_metadata, pub_test_data_source, title, authors)
    # assert res['success']
    # assert res['source_id'] == "_test_scourtas_example_iris_publish_{:.0f}_v1.1".format(timestamp)

    # check that pushing same dataset without update flag fails
    res = f.publish(pub_test_metadata, pub_test_data_source, title, authors, short_name=short_name)
    assert not res['success']

    # check that using update flag allows us to update dataset
    res = f.publish(pub_test_metadata, pub_test_data_source, title, authors, short_name=short_name, update=True)
    assert res['success']

    # check that using update flag for new dataset fails
    new_short_name = short_name + "_update"
    res = f.publish(pub_test_metadata, pub_test_data_source, title, authors, short_name=new_short_name, update=True)
    assert not res['success']


def test_check_status():
    # TODO: the 'active messages' in MDF CC's check_status() don't appear to do anything? need to determine how to test
    pass


def test_to_pytorch():
    f = Foundry(authorizers=auths, no_browser=True, no_local_server=True)
    
    _delete_test_data(f)

    f = f.load(test_dataset, download=True, globus=False, authorizers=auths)
    raw = f.load_data()

    ds = f.to_torch(split='train')
    
    assert raw['train'][0].iloc[0][0] == ds[0]['input'][0]
    assert len(raw['train'][0]) == len(ds)

    _delete_test_data(f)


def test_to_tensorflow():
    f = Foundry(authorizers=auths, no_browser=True, no_local_server=True)
    
    _delete_test_data(f)

    f = f.load(test_dataset, download=True, globus=False, authorizers=auths)
    raw = f.load_data()

    ds = f.to_tensorflow(split='train')
    
    assert raw['train'][0].iloc[0][0] == ds[0]['input'][0]
    assert len(raw['train'][0]) == len(ds)

    _delete_test_data(f)
