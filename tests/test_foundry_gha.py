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

def test_metadata_pull():
    f = Foundry(authorizers=res_cred)
    assert f.dc == {}
    f = f.load(test_dataset, download=False, authorizers=res_cred)
    assert f.dc["titles"][0]["title"] == expected_title
    #f = f.load(test_dataset, download=False)
    #assert f.dc["titles"][0]["title"] == expected_title
