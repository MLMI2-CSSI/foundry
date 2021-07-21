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


@pytest.mark.xfail(reason="Tests will fail in cloud")
def test_foundry_init_cloud():
    f = Foundry()
    assert isinstance(f.dlhub_client, DLHubClient)
    assert isinstance(f.forge_client, Forge)
    assert isinstance(f.connect_client, MDFConnectClient)

    f2 = Foundry(no_browser=False, no_local_server=True)
    assert isinstance(f2.dlhub_client, DLHubClient)
    assert isinstance(f2.forge_client, Forge)
    assert isinstance(f2.connect_client, MDFConnectClient)

    f3 = Foundry(no_browser=True, no_local_server=False)
    assert isinstance(f3.dlhub_client, DLHubClient)
    assert isinstance(f3.forge_client, Forge)
    assert isinstance(f3.connect_client, MDFConnectClient)


@pytest.mark.xfail(reason="Test should have a local endpoint, will fail cloud CI")
def test_download_globus():


    f = Foundry(no_browser=True, no_local_server=True)

    _delete_test_data(f)

    f = f .load(test_dataset, download=True)
    assert f.dc["titles"][0]["title"] == expected_title

    _delete_test_data(f)


def test_globus_dataframe_load():

    f = Foundry(no_browser=True, no_local_server=True)

    _delete_test_data(f)

    f = f.load(test_dataset, download=True)
    res = f.load_data()
    X, y = res['train']

    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)

    _delete_test_data(f)



def test_publish():
    # TODO: automate dealing with curation and cleaning after tests

    f = Foundry(no_browser=True, no_local_server=True)

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
