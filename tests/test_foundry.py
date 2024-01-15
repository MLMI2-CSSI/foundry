import json
import os
import shutil
import pytest
from filecmp import cmp
from datetime import datetime
from math import floor
import numpy as np
from pydantic import ValidationError
import requests
import mdf_toolbox
import pandas as pd
from mdf_forge import Forge
from foundry import Foundry
from foundry.auth import PubAuths
from foundry.https_upload import upload_to_endpoint
from globus_sdk import AuthClient
from mdf_connect_client import MDFConnectClient

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
confidential_login = (os.getenv("GITHUB_ACTIONS") or (client_id and client_secret))

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

if confidential_login:
    # Use confidential login if the tests are being run on GitHub Actions or
    # if a client ID and secret are provided
    auths = mdf_toolbox.confidential_login(client_id=client_id,
                                           client_secret=client_secret,
                                           services=services, make_clients=True)

    search_auth = mdf_toolbox.confidential_login(client_id=client_id,
                                                 client_secret=client_secret,
                                                 services=["search"], make_clients=False)
else:
    # Otherwise try to allow the user to login directly
    auths = mdf_toolbox.login(services=services, make_clients=True)
    search_auth = mdf_toolbox.login(services=["search"], make_clients=False)

auths['search_authorizer'] = search_auth['search']

# updated test dataset for publication
pub_test_dataset = "_test_foundry_iris_dev_v2.1"

pub_expected_title = "Iris Dataset"

# test dataset for all other tests
test_dataset = "elwood_md_v1.2"
test_doi = "10.18126/8p6m-e135"
expected_title = "Project Elwood: MD Simulated Monomer Properties"


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
    "keys": [
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


pub_test_invalid_metadata = {
    "keys": [
        {
            "key": ["sepal length (cm)"],
            "type": "input",
            "units": "cm",
            "description": 10
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

    if not confidential_login:

        f2 = Foundry(authorizers=auths, no_browser=False, no_local_server=True)
        assert isinstance(f2.forge_client, Forge)
        assert isinstance(f2.connect_client, MDFConnectClient)

        f3 = Foundry(authorizers=auths, no_browser=True, no_local_server=False)
        assert isinstance(f3.forge_client, Forge)
        assert isinstance(f3.connect_client, MDFConnectClient)


def test_list():
    f = Foundry(authorizers=auths)
    ds = f.list()
    assert isinstance(ds, pd.DataFrame)
    assert len(ds) > 0


def test_search():
    f = Foundry(authorizers=auths)
    q = "Elwood"
    ds = f.search(q)

    assert isinstance(ds, pd.DataFrame)
    assert len(ds) > 0
    assert ds.iloc[0]['name'] is not None
    assert ds.iloc[0]['source_id'] is not None
    assert ds.iloc[0]['year'] is not None


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


def test_dataframe_load_split():
    f = Foundry(authorizers=auths)
    _delete_test_data(f)
    f = f.load(test_dataset, download=True, globus=False, authorizers=auths)

    res = f.load_data(splits=['train'])
    X, y = res['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)
    _delete_test_data(f)


def test_dataframe_load_split_wrong_split_name():
    f = Foundry(authorizers=auths)
    _delete_test_data(f)
    f = f.load(test_dataset, download=True, globus=False, authorizers=auths)

    with pytest.raises(Exception) as exc_info:
        f.load_data(splits=['chewbacca'])

    err = exc_info.value
    assert hasattr(err, '__cause__')
    assert isinstance(err.__cause__, ValueError)
    _delete_test_data(f)


@pytest.mark.skip(reason='No clear examples of datasets without splits - likely to be protected against soon.')
def test_dataframe_load_split_but_no_splits():
    f = Foundry(authorizers=auths)
    _delete_test_data(f)
    f = f.load(test_dataset, download=True, globus=False, authorizers=auths)

    with pytest.raises(ValueError):
        f.load_data(splits=['train'])
    _delete_test_data(f)


def test_dataframe_load_doi():
    f = Foundry(authorizers=auths)
    _delete_test_data(f)
    f = f.load(test_doi, download=True, globus=False, authorizers=auths)

    res = f.load_data()
    X, y = res['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)
    _delete_test_data(f)


@pytest.mark.skipif(bool(confidential_login), reason="Test does not succeed on GHA - no Globus endpoint")
def test_download_globus():
    f = Foundry(authorizers=auths, no_browser=True, no_local_server=True)
    _delete_test_data(f)
    f = f.load(test_dataset, download=True)

    assert f.dc["titles"][0]["title"] == expected_title
    _delete_test_data(f)


@pytest.mark.skipif(bool(confidential_login), reason="Test does not succeed on GHA - no Globus endpoint")
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


@pytest.mark.skipif(bool(confidential_login), reason="Not run as part of GHA CI")
def test_publish_with_https():
    """System test: Assess the end-to-end publication of a dataset via HTTPS
    """

    f = Foundry(index="mdf-test", authorizers=auths)
    timestamp = datetime.now().timestamp()
    title = "https_publish_test_{:.0f}".format(timestamp)
    short_name = "https_pub_{:.0f}".format(timestamp)
    authors = ["A Scourtas"]
    local_path = "./data/https_test"

    # create test JSON to upload (if it doesn't already exist)
    _write_test_data(local_path)

    res = f.publish_dataset(pub_test_metadata, title, authors, https_data_path=local_path, short_name=short_name)

    assert res['success']
    assert res['source_id'] == f"_test_{short_name}_v1.1"


def test_publish_invalid_metadata():
    """Testing the validation of the metadata when publishing data
    """
    with pytest.raises(ValidationError) as exc_info:
        f = Foundry(index="mdf-test", authorizers=auths)
        timestamp = datetime.now().timestamp()
        title = "https_publish_test_{:.0f}".format(timestamp)
        short_name = "https_pub_{:.0f}".format(timestamp)
        authors = ["A Scourtas"]
        local_path = "./data/https_test"

        # create test JSON to upload (if it doesn't already exist)
        _write_test_data(local_path)
        f.publish_dataset(pub_test_invalid_metadata, title, authors, https_data_path=local_path, short_name=short_name)

    assert exc_info.value.errors()[0]['msg'] == 'str type expected'


def test_upload_to_endpoint():
    """Unit test: Test the _upload_to_endpoint() HTTPS functionality on its own, without publishing to MDF
    """
    endpoint_id = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec"  # NCSA endpoint
    dest_parent = "/tmp"
    dest_child = f"test_{floor(datetime.now().timestamp())}"
    local_path = "./data/https_test"
    filename = "test_data.json"

    f = Foundry(index="mdf-test", authorizers=auths)
    # create test JSON to upload (if it doesn't already exist)
    _write_test_data(local_path, filename)

    # gather auth'd clients necessary for publication to endpoint
    endpoint_id = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec"  # NCSA endpoint
    scope = f"https://auth.globus.org/scopes/{endpoint_id}/https"  # lets you HTTPS to specific endpoint
    pub_auths = PubAuths(
        transfer_client=f.auths["transfer"],
        auth_client_openid=AuthClient(authorizer=f.auths['openid']),
        endpoint_auth_clients={endpoint_id: AuthClient(authorizer=f.auths[scope])}
    )
    # upload via HTTPS to NCSA endpoint
    globus_data_source = upload_to_endpoint(pub_auths, local_path, endpoint_id, dest_parent=dest_parent,
                                            dest_child=dest_child)

    expected_data_source = f"https://app.globus.org/file-manager?origin_id=82f1b5c6-6e9b-11e5-ba47-22000b92c6ec&" \
                           f"origin_path=%2Ftmp%2F{dest_child}"
    # confirm data source link was created properly, with correct folders
    assert globus_data_source == expected_data_source

    mdf_url = f"https://data.materialsdatafacility.org/tmp/{dest_child}/{filename}"
    response = requests.get(mdf_url)
    # check that we get a valid response back (note that a 200 could be a UI error, returned as HTML)
    assert response.status_code == 200
    # check that contents of response are as expected
    tmp_file = "./data/tmp_data.json"
    with open(tmp_file, "wb") as fl:
        fl.write(response.content)
    assert cmp(tmp_file, os.path.join(local_path, filename))


def _write_test_data(dest_path="./data/https_test", filename="test_data.json"):
    # Create random JSON data
    data = pd.DataFrame(np.random.rand(100, 4), columns=list('ABCD'))
    res = data.to_json(orient="records")

    # Make data directory
    os.makedirs(dest_path, exist_ok=True)
    data_filepath = os.path.join(dest_path, filename)

    # Write data to JSON file
    with open(data_filepath, "w+") as f:
        json.dump(res, f, indent=4)


def test_ACL_creation_and_deletion():
    pass


@pytest.mark.skipif(bool(confidential_login), reason="Not run as part of GHA CI")
def test_publish_with_globus():
    # TODO: automate dealing with curation and cleaning after tests

    f = Foundry(authorizers=auths, index="mdf-test", no_browser=True, no_local_server=True)

    timestamp = datetime.now().timestamp()
    title = "scourtas_example_iris_test_publish_{:.0f}".format(timestamp)
    short_name = "example_AS_iris_test_{:.0f}".format(timestamp)
    authors = ["A Scourtas"]

    res = f.publish_dataset(pub_test_metadata, title, authors, globus_data_source=pub_test_data_source,
                            short_name=short_name)

    # publish with short name
    assert res['success']
    assert res['source_id'] == "_test_example_iris_{:.0f}_v1.1".format(timestamp)

    # TODO: publish with long title -- for some reason even when I change the title, it still says it's already pub'd
    # title += "long"
    # res = f.publish(pub_test_metadata, pub_test_data_source, title, authors)
    # assert res['success']
    # assert res['source_id'] == "_test_scourtas_example_iris_publish_{:.0f}_v1.1".format(timestamp)

    # check that pushing same dataset without update flag fails
    res = f.publish_dataset(pub_test_metadata, title, authors, globus_data_source=pub_test_data_source, short_name=short_name)
    assert not res['success']

    # check that using update flag allows us to update dataset
    res = f.publish_dataset(pub_test_metadata, title, authors, globus_data_source=pub_test_data_source, short_name=short_name, update=True)
    assert res['success']

    # check that using update flag for new dataset fails
    new_short_name = short_name + "_update"
    res = f.publish_dataset(pub_test_metadata, title, authors, globus_data_source=pub_test_data_source, short_name=new_short_name,  update=True)
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
