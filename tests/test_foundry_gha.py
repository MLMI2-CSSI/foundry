import os, shutil
import re
import types
import pytest
from datetime import datetime
import mdf_toolbox
import pandas as pd
from mdf_forge import Forge
from foundry import Foundry
from dlhub_sdk import DLHubClient
from mdf_connect_client import MDFConnectClient


#github specific declarations
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
services= [
            "data_mdf",
            "mdf_connect",
            "search",
            "petrel",
            "transfer",
            "dlhub",
            "openid",
            "https://auth.globus.org/scopes/facd7ccc-c5f4-42aa-916b-a0e270e2c2a9/all",]

res_cred = mdf_toolbox.confidential_login(client_id=client_id,
                                        client_secret=client_secret,
                                        services=services, make_clients=True)


#updated test dataset
test_dataset = "_test_foundry_iris_dev_v2.1"
expected_title = "Iris Dataset"

#Kept the Old metadata format in case we ever want to refer back
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


test_metadata = {
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
# Globus endpoint for '_iris_dev'
test_data_source = "https://app.globus.org/file-manager?origin_id=e38ee745-6d04-11e5-ba46-22000b92c6ec&origin_path=%2Ffoundry-test%2Firis-dev%2F"


#Quick function to delete any downloaded test data
def _delete_test_data(foundry_obj):
    path = os.path.join(foundry_obj.config.local_cache_dir, test_dataset)
    if os.path.isdir(path):
        shutil.rmtree(path)



def test_foundry_init_cloud():
    f1 = Foundry(no_browser=True, no_local_server=True, authorizers=res_cred)
    assert isinstance(f1.dlhub_client, DLHubClient)
    assert isinstance(f1.forge_client, Forge)
    assert isinstance(f1.connect_client, MDFConnectClient)


@pytest.mark.xfail(reason="Tests will fail in cloud")
def test_foundry_init_cloud():
    f = Foundry(authorizers=res_cred)
    assert isinstance(f.dlhub_client, DLHubClient)
    assert isinstance(f.forge_client, Forge)
    assert isinstance(f.connect_client, MDFConnectClient)

    f2 = Foundry(no_browser=False, no_local_server=True, authorizers=res_cred)
    assert isinstance(f2.dlhub_client, DLHubClient)
    assert isinstance(f2.forge_client, Forge)
    assert isinstance(f2.connect_client, MDFConnectClient)

    f3 = Foundry(no_browser=True, no_local_server=False, authorizers=res_cred)
    assert isinstance(f3.dlhub_client, DLHubClient)
    assert isinstance(f3.forge_client, Forge)
    assert isinstance(f3.connect_client, MDFConnectClient)


def test_list():
    f = Foundry(no_browser=True, no_local_server=True, authorizers=res_cred)
    ds = f.list()
    assert isinstance(ds, pd.DataFrame)
    assert len(ds) > 0


def test_metadata_pull():
    f = Foundry(no_browser=True, no_local_server=True, authorizers=res_cred)
    f = f.load(test_dataset, download=False)
    assert f.dc["titles"][0]["title"] == expected_title


@pytest.mark.xfail(reason="Test should have a local endpoint, will fail cloud CI")
def test_download_globus():


    f = Foundry(no_browser=True, no_local_server=True, authorizers=res_cred)

    _delete_test_data(f)

    f = f .load(test_dataset, download=True)
    assert f.dc["titles"][0]["title"] == expected_title

    _delete_test_data(f)



def test_download_https():

    f = Foundry(no_browser=True, no_local_server=True, authorizers=res_cred)

    _delete_test_data(f)

    f = f.load(test_dataset, download=True, globus=False)
    assert f.dc["titles"][0]["title"] == expected_title

    _delete_test_data(f)


def test_dataframe_load():

    f = Foundry(no_browser=True, no_local_server=True, authorizers=res_cred)

    _delete_test_data(f)

    f = f.load(test_dataset, download=True, globus=False)
    res = f.load_data()
    X, y = res['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)

    _delete_test_data(f)


def test_publish():
    # TODO: automate dealing with curation and cleaning after tests

    f = Foundry(no_browser=True, no_local_server=True, authorizers=res_cred)

    timestamp = datetime.now().timestamp()
    title = "scourtas_example_iris_test_publish_{:.0f}".format(timestamp)
    short_name = "example_AS_iris_test_{:.0f}".format(timestamp)
    authors = ["A Scourtas"]

    res = f.publish(test_metadata, test_data_source, title, authors, short_name=short_name)

    # publish with short name
    assert res['success']
    assert res['source_id'] == "_test_example_iris_{:.0f}_v1.1".format(timestamp)

    # TODO: publish with long title -- for some reason even when I change the title, it still says it's already pub'd
    # title += "long"
    # res = f.publish(test_metadata, test_data_source, title, authors)
    # assert res['success']
    # assert res['source_id'] == "_test_scourtas_example_iris_publish_{:.0f}_v1.1".format(timestamp)

    # check that pushing same dataset without update flag fails
    res = f.publish(test_metadata, test_data_source, title, authors, short_name=short_name)
    assert not res['success']

    # check that using update flag allows us to update dataset
    res = f.publish(test_metadata, test_data_source, title, authors, short_name=short_name, update=True)
    assert res['success']

    # check that using update flag for new dataset fails
    new_short_name = short_name + "_update"
    res = f.publish(test_metadata, test_data_source, title, authors, short_name=new_short_name, update=True)
    assert not res['success']


def test_check_status():
    # TODO: the 'active messages' in MDF CC's check_status() don't appear to do anything? need to determine how to test
    pass


# # Helper
# # Return codes:
# #  -1: No match, the value was never found
# #   0: Exclusive match, no values other than argument found
# #   1: Inclusive match, some values other than argument found
# #   2: Partial match, value is found in some but not all results
# # def check_field(res, field, regex):
# #     dict_path = ""
# #     for key in field.split("."):
# #         if key == "[]":
# #             dict_path += "[0]"
# #         else:
# #             dict_path += ".get('{}', {})".format(key, "{}")
# #     # If no results, set matches to false
# #     all_match = len(res) > 0
# #     only_match = len(res) > 0
# #     some_match = False
# #     for r in res:
# #         vals = eval("r" + dict_path)
# #         if vals == {}:
# #             vals = []
# #         elif type(vals) is not list:
# #             vals = [vals]
# #         # If a result does not contain the value, no match
# #         if regex not in vals and not any(
# #             [re.search(str(regex), str(value)) for value in vals]
# #         ):
# #             all_match = False
# #             only_match = False
# #         # If a result contains other values, inclusive match
# #         elif len(vals) != 1:
# #             only_match = False
# #             some_match = True
# #         else:
# #             some_match = True
#
# #     if only_match:
# #         # Exclusive match
# #         return 0
# #     elif all_match:
# #         # Inclusive match
# #         return 1
# #     elif some_match:
# #         # Partial match
# #         return 2
# #     else:
# #         # No match
# #         return -1
