import os
import shutil
from datetime import datetime
from math import floor

import numpy as np
import pandas as pd
import pytest
import requests
from filecmp import cmp
from globus_sdk import AuthClient
from mdf_connect_client import MDFConnectClient
import mock
import json
import builtins

import mdf_toolbox
from mdf_forge import Forge
from foundry import foundry
from foundry.foundry_dataset import FoundryDataset
from foundry.auth import PubAuths
from foundry.https_upload import upload_to_endpoint
from tests.test_data import datacite_data, valid_metadata, invalid_metadata



client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
is_gha = os.getenv("GITHUB_ACTIONS")

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

# Globus endpoint for '_iris_dev' for test publication
pub_test_data_source = "https://app.globus.org/file-manager?origin_id=e38ee745-6d04-11e5-ba46-22000b92c6ec&origin_path=%2Ffoundry-test%2Firis-dev%2F"


# Quick function to delete any downloaded test data
def _delete_test_data(dataset):
    path = os.path.join(dataset._foundry_cache.local_cache_dir, test_dataset)
    if os.path.isdir(path):
        shutil.rmtree(path)


def test_foundry_init():
    f = foundry.Foundry(authorizers=auths)
    assert isinstance(f.forge_client, Forge)
    assert isinstance(f.connect_client, MDFConnectClient)

    if not is_gha:

        f2 = foundry.Foundry(download=False, authorizers=auths, no_browser=False, no_local_server=True)
        assert isinstance(f2.forge_client, Forge)
        assert isinstance(f2.connect_client, MDFConnectClient)

        f3 = foundry.Foundry(download=False, authorizers=auths, no_browser=True, no_local_server=False)
        assert isinstance(f3.forge_client, Forge)
        assert isinstance(f3.connect_client, MDFConnectClient)


def test_list():
    f = foundry.Foundry(authorizers=auths)
    ds = f.list()
    # assert isinstance(ds, pd.DataFrame)
    assert len(ds) > 0


def test_search():
    f = foundry.Foundry(authorizers=auths)
    q = "Elwood"
    ds = f.search(q)

    assert isinstance(ds, pd.DataFrame)
    assert len(ds) > 0

    dataset = ds.iloc[0].FoundryDataset

    # assert ds.iloc[0]['name'] is not None
    assert dataset.dc.titles[0].title is not None

    # assert ds.iloc[0]['source_id'] is not None
    assert dataset.dataset_name is not None

    # assert ds.iloc[0]['year'] is not None
    assert dataset.dc.publicationYear is not None


def test_dataset_get_citation():
    f = foundry.Foundry(authorizers=auths)
    ds = f.search(test_dataset).iloc[0].FoundryDataset
    assert ds.get_citation() is not None


def test_search_as_list():
    f = foundry.Foundry(authorizers=auths)
    q = "Elwood"
    ds = f.search(q, as_list=True)

    assert isinstance(ds, list)
    assert len(ds) > 0

    dataset = ds[0]

    # assert ds[0]['name'] is not None
    assert dataset.dc.titles[0].title is not None

    # assert ds[0]['source_id'] is not None
    assert dataset.dataset_name is not None

    # assert ds[0]['year'] is not None
    assert dataset.dc.publicationYear is not None


def test_search_limit():
    f = foundry.Foundry(authorizers=auths)
    ds = f.search(limit=10)

    assert isinstance(ds, pd.DataFrame)
    assert len(ds) == 10

    dataset = ds.iloc[0].FoundryDataset

    # assert ds.iloc[0]['name'] is not None
    assert dataset.dc.titles[0].title is not None

    # assert ds.iloc[0]['source_id'] is not None
    assert dataset.dataset_name is not None

    # assert ds.iloc[0]['year'] is not None
    assert dataset.dc.publicationYear is not None


def test_metadata_pull():
    f = foundry.Foundry(download=False, authorizers=auths)
    dataset = f.search(test_dataset).iloc[0].FoundryDataset
    assert dataset.dc.titles[0].title == expected_title


@pytest.mark.skipif(bool(is_gha), reason="Test does not succeed on GHA - no Globus endpoint")
def test_download_globus():
    f = foundry.Foundry(globus=False, authorizers=auths)
    dataset = f.search(test_dataset).iloc[0].FoundryDataset
    res = dataset.get_as_dict()
    X, y = res['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)
    _delete_test_data(dataset)


@pytest.mark.skip("Skipping until we can get HTTPS working on new PR")
def test_download_https():
    f = foundry.Foundry(globus=False, authorizers=auths)
    dataset = f.search(test_dataset).iloc[0].FoundryDataset
    res = dataset.get_as_dict()
    X, y = res['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)
    _delete_test_data(dataset)


def test_delete_cache():
    f = foundry.Foundry(globus=True, authorizers=auths)
    dataset = f.search(test_dataset).iloc[0].FoundryDataset

    with mock.patch.object(builtins, 'input', lambda _: 'y'):
        dataset.clear_dataset_cache()

    assert os.path.exists(os.path.join(dataset._foundry_cache.local_cache_dir, dataset.dataset_name)) is False


@pytest.mark.skip(reason='Saving for #401')
def test_dataframe_load_split():
    f = foundry.Foundry(test_dataset, download=True, globus=False, authorizers=auths)

    dataset = f.load_data(splits=['train'])
    X, y = dataset['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)
    _delete_test_data(dataset)


@pytest.mark.skip(reason='Saving for #401')
def test_dataframe_load_split_wrong_split_name():
    f = foundry.Foundry(download=True, globus=False, authorizers=auths)

    with pytest.raises(Exception) as exc_info:
        dataset = f.load_data(splits=['chewbacca'])

    err = exc_info.value
    assert hasattr(err, '__cause__')
    assert isinstance(err.__cause__, ValueError)
    _delete_test_data(dataset)


@pytest.mark.skip(reason='No clear examples of datasets without splits - likely to be protected against soon.')
def test_dataframe_load_split_but_no_splits():
    f = foundry.Foundry(test_dataset, download=True, globus=False, authorizers=auths)

    with pytest.raises(ValueError):
        dataset = f.load_data(splits=['train'])
    _delete_test_data(dataset)


def test_dataframe_search_by_doi():
    f = foundry.Foundry(globus=False, authorizers=auths)

    result = f.search(test_doi)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert isinstance(result.iloc[0].FoundryDataset, foundry.FoundryDataset)
    _delete_test_data(result.iloc[0].FoundryDataset)


@pytest.mark.skipif(bool(is_gha), reason="Test does not succeed on GHA - no Globus endpoint")
def test_dataframe_download_by_doi():
    f = foundry.Foundry(globus=True, authorizers=auths, no_browser=True)
    datasets = f.search(test_doi)
    dataset = datasets.iloc[0].FoundryDataset
    dataset_dict = dataset.get_as_dict()
    X, y = dataset_dict['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)
    _delete_test_data(dataset)


@pytest.mark.skip(reason='Omitting testing beyond search functionality until next story')
@pytest.mark.skipif(bool(is_gha), reason="Test does not succeed on GHA - no Globus endpoint")
def test_globus_dataframe_load():
    f = foundry.Foundry(test_dataset, download=True, authorizers=auths, no_browser=True, no_local_server=True)

    dataset = f.load_data()
    X, y = dataset['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)
    _delete_test_data(dataset)


# @pytest.mark.skipif(bool(is_gha), reason="Not run as part of GHA CI")
# def test_publish_with_https():
#     """System test: Assess the end-to-end publication of a dataset via HTTPS
#     """

#     f = foundry.Foundry(index="mdf-test",
#                         download=True,
#                         globus=False,
#                         authorizers=auths)
    
#     timestamp = datetime.now().timestamp()
#     short_name = "https_peanuts_pub_{:.0f}".format(timestamp)
#     local_path = "./data/https_test"

#     ds = FoundryDataset(dataset_name=short_name,
#                         foundry_schema=valid_metadata,
#                         datacite_entry=datacite_data)

#     ds.add_data(local_data_path=local_path)

#     # create test JSON to upload (if it doesn't already exist)
#     _write_test_data(local_path)

#     res = f.publish_dataset(ds)

#     assert res['success']
#     assert res['source_id'] == f'{short_name}-test'


# @pytest.mark.skip(reason='Publishing has not yet been re-implemented following refactoring')
def test_publish_invalid_metadata():
    """Testing the validation of the metadata when publishing data
    """
    with pytest.raises(Exception) as exc_info:
        timestamp = datetime.now().timestamp()
        short_name = "https_pub_{:.0f}".format(timestamp)
        local_path = "./data/https_test"

        f = foundry.Foundry(index="mdf-test", authorizers=auths)

        # create dataset to publish

        ds = FoundryDataset(dataset_name='peanuts',
                            foundry_schema=invalid_metadata,
                            datacite_entry=datacite_data)

        ds.add_data(local_data_path=local_path)

        # create test JSON to upload (if it doesn't already exist)
        _write_test_data(local_path)
        f.publish_dataset(ds, short_name=short_name, test=True)

    assert exc_info.value is not None


def test_upload_to_endpoint():
    """Unit test: Test the _upload_to_endpoint() HTTPS functionality on its own, without publishing to MDF
    """
    endpoint_id = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec"  # NCSA endpoint
    dest_parent = "/tmp"
    dest_child = f"test_{floor(datetime.now().timestamp())}"
    local_path = "./data/https_test"
    filename = "test_data.json"

    f = foundry.Foundry(index="mdf-test", authorizers=auths)
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


@pytest.mark.skip(reason='Not sure what this is')
def test_ACL_creation_and_deletion():
    pass


@pytest.mark.skip(reason='Publishing has not yet been re-implemented following refactoring')
@pytest.mark.skipif(bool(is_gha), reason="Not run as part of GHA CI")
def test_publish_with_globus():
    # TODO: automate dealing with curation and cleaning after tests

    f = foundry.Foundry(authorizers=auths, index="mdf-test", no_browser=True, no_local_server=True)

    timestamp = datetime.now().timestamp()
    title = "scourtas_example_iris_test_publish_{:.0f}".format(timestamp)
    short_name = "example_AS_iris_test_{:.0f}".format(timestamp)
    authors = ["A Scourtas"]

    res = f.publish_dataset(valid_metadata, title, authors, globus_data_source=pub_test_data_source,
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
    res = f.publish_dataset(valid_metadata, title, authors, globus_data_source=pub_test_data_source, short_name=short_name)
    assert not res['success']

    # check that using update flag allows us to update dataset
    res = f.publish_dataset(valid_metadata, title, authors, globus_data_source=pub_test_data_source, short_name=short_name, update=True)
    assert res['success']

    # check that using update flag for new dataset fails
    new_short_name = short_name + "_update"
    res = f.publish_dataset(valid_metadata, title, authors, globus_data_source=pub_test_data_source, short_name=new_short_name,  update=True)
    assert not res['success']


@pytest.mark.skip(reason='Not sure what this is')
def test_check_status():
    # TODO: the 'active messages' in MDF CC's check_status() don't appear to do anything? need to determine how to test
    pass


@pytest.mark.skip(reason='Omitting testing beyond search functionality until next story')
def test_to_pytorch():
    f = foundry.Foundry(test_dataset, download=True, globus=False, authorizers=auths, no_browser=True, no_local_server=True)

    raw = f.load_data()

    ds = f.to_torch(split='train')

    assert raw['train'][0].iloc[0][0] == ds[0]['input'][0]
    assert len(raw['train'][0]) == len(ds)

    _delete_test_data(ds)


@pytest.mark.skip(reason='Omitting testing beyond search functionality until next story')
def test_to_tensorflow():
    f = foundry.Foundry(test_dataset, download=True, globus=False, authorizers=auths, no_browser=True, no_local_server=True)

    raw = f.load_data()

    ds = f.to_tensorflow(split='train')

    assert raw['train'][0].iloc[0][0] == ds[0]['input'][0]
    assert len(raw['train'][0]) == len(ds)

    _delete_test_data(ds)
