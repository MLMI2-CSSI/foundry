import json
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import MagicMock

from . import test_foundry_dataset
from foundry.jsonschema_models.project_model import Split as FoundrySplit, \
                                  Key as FoundryKey
from foundry.foundry_cache import FoundryCache
from foundry.models import FoundrySchema


@pytest.fixture
def mock_foundry_cache():
    cache_dir = str(Path(__file__).parent) + '/test_data'
    cache = FoundryCache(forge_client=MagicMock(), 
                         transfer_client=MagicMock(), 
                         local_cache_dir=cache_dir,
                         use_globus=False,
                         interval=10,
                         parallel_https=4,
                         verbose=False)
    return cache


@pytest.fixture
def mock_nonexistent_foundry_cache():
    cache_dir = str(Path(__file__).parent) + '/cheeseballs'
    cache = FoundryCache(forge_client=MagicMock(), 
                         transfer_client=MagicMock(), 
                         local_cache_dir=cache_dir,
                         use_globus=False,
                         interval=10,
                         parallel_https=4,
                         verbose=False)
    return cache


def test_validate_local_dataset_storage_exists(mock_foundry_cache):
    cache = mock_foundry_cache
    dataset_name = "elwood_md_v1.2"
    assert cache.validate_local_dataset_storage(dataset_name) is True


def test_validate_local_dataset_storage_missing_files(mock_foundry_cache):
    cache = mock_foundry_cache
    dataset_name = "elwood_md_v1.2"
    # Create a split with a missing file
    splits = [
        FoundrySplit(path="file1.csv", type="train"),
        FoundrySplit(path="file2.csv", type="test"),
        FoundrySplit(path="file3.csv", type="validation")
    ]

    assert cache.validate_local_dataset_storage(dataset_name, splits) is False


def test_validate_local_dataset_storage_complete(mock_foundry_cache):
    cache = mock_foundry_cache
    dataset_name = "elwood_md_v1.2"

    assert cache.validate_local_dataset_storage(dataset_name) is True


def test_validate_local_dataset_storage_not_present(mock_nonexistent_foundry_cache):
    cache = mock_nonexistent_foundry_cache
    dataset_name = "test_dataset"

    assert cache.validate_local_dataset_storage(dataset_name) is False


@pytest.fixture
def mock_tabular_foundry_source_id():
    source_id = "elwood_md_v1.2"
    yield source_id


@pytest.fixture
def mock_tabular_foundry_schema():
    foundry_schema = json.loads('{"short_name": "elwood_properties", "data_type": "tabular", "task_type": ["unsupervised", "generative", "supervised"], "domain": ["materials science", "chemistry", "simulation"], "n_items": 410.0, "splits": [{"type": "train", "path": "MD_properties.csv", "label": "train"}], "keys": [{"key": ["SMILES"], "type": "input", "filter": null, "description": "Canonical SMILES string of molecule", "units": "arb", "classes": null}, {"key": ["E_coh (MPa)"], "type": "target", "filter": null, "description": "Simulated cohesive energy (in MPa)", "units": "MPa", "classes": null}, {"key": ["T_g (K)"], "type": "target", "filter": null, "description": "Simulated glass transition temperature (in Kelvin)", "units": "Kelvin", "classes": null}, {"key": ["R_gyr (A^2)"], "type": "target", "filter": null, "description": "Simulated squared radius of gyration (in Angstroms^2)", "units": "Angstrom^2", "classes": null}, {"key": ["Densities (kg/m^3)"], "type": "target", "filter": null, "description": "Simulated density (in kg/m^3)", "units": "kg/m^3", "classes": null}]}')
    yield foundry_schema


@pytest.fixture
def mock_hdf5_foundry_source_id():
    source_id = "test_dataset"
    yield source_id


@pytest.fixture
def mock_hdf5_foundry_schema():
    foundry_schema = json.loads('{"short_name": "elwood_properties", "data_type": "hdf5", "task_type": ["unsupervised", "generative", "supervised"], "domain": ["materials science", "chemistry", "simulation"], "n_items": 410.0, "splits": [{"type": "train", "path": "MD_properties.csv", "label": "train"}], "keys": [{"key": ["SMILES"], "type": "input", "filter": null, "description": "Canonical SMILES string of molecule", "units": "arb", "classes": null}, {"key": ["E_coh (MPa)"], "type": "target", "filter": null, "description": "Simulated cohesive energy (in MPa)", "units": "MPa", "classes": null}, {"key": ["T_g (K)"], "type": "target", "filter": null, "description": "Simulated glass transition temperature (in Kelvin)", "units": "Kelvin", "classes": null}, {"key": ["R_gyr (A^2)"], "type": "target", "filter": null, "description": "Simulated squared radius of gyration (in Angstroms^2)", "units": "Angstrom^2", "classes": null}, {"key": ["Densities (kg/m^3)"], "type": "target", "filter": null, "description": "Simulated density (in kg/m^3)", "units": "kg/m^3", "classes": null}]}')
    yield foundry_schema


@pytest.fixture
def mock_read_functions():

    def mock_read_csv(file_path):
        # Mock _read_csv() to return a DataFrame with minimal example data
        data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
        return pd.DataFrame(data)

    def mock_read_json(file_path):
        # Mock _read_json() to return a DataFrame with minimal example data
        data = {'Column1': [4, 5, 6], 'Column2': ['D', 'E', 'F']}
        return pd.DataFrame(data)

    def mock_read_excel(file_path):
        # Mock _read_excel() to return a DataFrame with minimal example data
        data = {'Column1': [7, 8, 9], 'Column2': ['G', 'H', 'I']}
        return pd.DataFrame(data)

    # # Patch the _read_csv(), _read_json(), and _read_excel() functions with the mock functions
    # with patch('foundry.foundry_cache._read_csv', MagicMock(side_effect=mock_read_csv)):
    #     with patch('foundry.foundry_cache._read_json', MagicMock(side_effect=mock_read_json)):
    #         with patch('foundry.foundry_cache._read_excel', MagicMock(side_effect=mock_read_excel)):
    #             yield


def test_load_data_with_globus(mock_foundry_cache,
                               mock_tabular_foundry_source_id,
                               mock_tabular_foundry_schema):
    cache = mock_foundry_cache
    source_id = mock_tabular_foundry_source_id
    foundry_schema = FoundrySchema(mock_tabular_foundry_schema)
    cache._load_data(foundry_schema,
                     file="MD_properties.csv",
                     source_id=source_id,
                     as_hdf5=False)
    # Add assertions here


def test_load_data_with_hdf5(mock_foundry_cache,
                             mock_hdf5_foundry_schema,
                             mock_read_functions,
                             mock_hdf5_foundry_source_id):
    cache = mock_foundry_cache
    source_id = mock_hdf5_foundry_source_id
    foundry_schema = FoundrySchema(mock_hdf5_foundry_schema)
    cache._load_data(foundry_schema,
                     file="elwood.hdf5",
                     source_id=source_id,
                     as_hdf5=True)
    # Add assertions here


def test_load_data_with_globus_2(mock_foundry_cache,
                                 mock_tabular_foundry_schema,
                                 mock_read_functions,
                                 mock_tabular_foundry_source_id):
    cache = mock_foundry_cache
    source_id = mock_tabular_foundry_source_id
    foundry_schema = FoundrySchema(mock_tabular_foundry_schema)
    cache._load_data(foundry_schema,
                     file="MD_properties.csv",
                     source_id=source_id,
                     as_hdf5=False)
    # Add assertions here


def test_load_data_with_source_id(mock_foundry_cache,
                                  mock_tabular_foundry_schema,
                                  mock_read_functions,
                                  mock_hdf5_foundry_source_id):
    cache = mock_foundry_cache
    foundry_schema = FoundrySchema(mock_tabular_foundry_schema)
    with pytest.raises(Exception) as exc_info:
        cache._load_data(foundry_schema, 
                         file="MD_properties.csv", 
                         source_id="12345", 
                         as_hdf5=False)
    err = exc_info.value
    assert isinstance(err, FileNotFoundError)
