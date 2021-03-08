import os
import re
import types
import pytest
import mdf_toolbox
import pandas as pd
from mdf_forge import Forge
from foundry import Foundry
from dlhub_sdk import DLHubClient

test_dataset = "_test_blaiszik_foundry_iris_v2.1"
expected_title = "Foundry - Iris Dataset"


def test_foundry_init_cloud():
    f1 = Foundry(no_browser=True, no_local_server=True)
    assert isinstance(f1.dlhub_client, DLHubClient)
    assert isinstance(f1.forge_client, Forge)


@pytest.mark.xfail(reason="Tests will fail in cloud")
def test_foundry_init_cloud():
    f = Foundry()
    assert isinstance(f.dlhub_client, DLHubClient)
    assert isinstance(f.forge_client, Forge)

    f2 = Foundry(no_browser=False, no_local_server=True)
    assert isinstance(f2.dlhub_client, DLHubClient)
    assert isinstance(f2.forge_client, Forge)

    f3 = Foundry(no_browser=True, no_local_server=False)
    assert isinstance(f3.dlhub_client, DLHubClient)
    assert isinstance(f3.forge_client, Forge)


def test_list():
    f = Foundry(no_browser=True, no_local_server=True)
    ds = f.list()
    assert isinstance(ds, pd.DataFrame)
    assert len(ds) > 0


def test_metadata_pull():
    f = Foundry(no_browser=True, no_local_server=True)
    f = f.load(test_dataset, download=False)
    assert f.dc["titles"][0]["title"] == expected_title


@pytest.mark.xfail(reason="Test should have a local endpoint, will fail cloud CI")
def test_download_globus():
    f = Foundry(no_browser=True, no_local_server=True)
    f = f.load(test_dataset, download=True)
    assert f.dc["titles"][0]["title"] == expected_title


def test_data_pull():
    f = Foundry(no_browser=True, no_local_server=True)
    f = f.load(test_dataset, download=True, globus=False)
    assert f.dc["titles"][0]["title"] == expected_title


def test_download_https():
    f = Foundry(no_browser=True, no_local_server=True)
    f = f.load(test_dataset, download=True)
    assert f.dc["titles"][0]["title"] == expected_title


def test_dataframe_load():
    f = Foundry(no_browser=True, no_local_server=True)
    f = f.load(test_dataset, download=True)
    X, y = f.load_data()
    assert len(X) > 1
    assert isinstance(X, pd.DataFrame)
    assert len(y) > 1
    assert isinstance(y, pd.DataFrame)


# Helper
# Return codes:
#  -1: No match, the value was never found
#   0: Exclusive match, no values other than argument found
#   1: Inclusive match, some values other than argument found
#   2: Partial match, value is found in some but not all results
# def check_field(res, field, regex):
#     dict_path = ""
#     for key in field.split("."):
#         if key == "[]":
#             dict_path += "[0]"
#         else:
#             dict_path += ".get('{}', {})".format(key, "{}")
#     # If no results, set matches to false
#     all_match = len(res) > 0
#     only_match = len(res) > 0
#     some_match = False
#     for r in res:
#         vals = eval("r" + dict_path)
#         if vals == {}:
#             vals = []
#         elif type(vals) is not list:
#             vals = [vals]
#         # If a result does not contain the value, no match
#         if regex not in vals and not any(
#             [re.search(str(regex), str(value)) for value in vals]
#         ):
#             all_match = False
#             only_match = False
#         # If a result contains other values, inclusive match
#         elif len(vals) != 1:
#             only_match = False
#             some_match = True
#         else:
#             some_match = True

#     if only_match:
#         # Exclusive match
#         return 0
#     elif all_match:
#         # Inclusive match
#         return 1
#     elif some_match:
#         # Partial match
#         return 2
#     else:
#         # No match
#         return -1
