from pathlib import Path
import pytest
from unittest.mock import MagicMock

from foundry.models import FoundrySplit, FoundrySchema, FoundryKey
from foundry.foundry_cache import FoundryCache
import pandas as pd


@pytest.fixture
def mock_foundry_cache():
    cache_dir = str(Path(__file__).parent) + '/test_data'
    cache = FoundryCache(forge_client=MagicMock(), transfer_client=MagicMock(), local_cache_dir=cache_dir)
    # cache.validate_local_dataset_storage = MagicMock(return_value=True)  # Mock the validation method
    return cache


@pytest.fixture
def mock_nonexistent_foundry_cache():
    cache_dir = str(Path(__file__).parent) + '/cheeseballs'
    cache = FoundryCache(forge_client=MagicMock(), transfer_client=MagicMock(), local_cache_dir=cache_dir)
    # cache.validate_local_dataset_storage = MagicMock(return_value=True)  # Mock the validation method
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
def mock_tabular_foundry_schema():
    # foundry_key_1 = FoundryKey(key=["column1", "column2"], type='input')
    # foundry_key_2 = FoundryKey(key=["column2", "column4"], type='output')
    foundry_key_1 = FoundryKey(
        key=['SMILES'],
        type='input',
        classes=None,
        description='Canonical SMILES string of molecule',
        filter=None,
        units='arb'
    )
    foundry_key_2 = FoundryKey(
        key=['E_coh (MPa)'],
        type='target',
        classes=None,
        description='Simulated cohesive energy (in MPa)',
        filter=None,
        units='MPa'
    )
    foundry_key_3 = FoundryKey(
        key=['T_g (K)'],
        type='target',
        classes=None,
        description='Simulated glass transition temperature (in Kelvin)',
        filter=None,
        units='Kelvin'
    )
    foundry_key_4 = FoundryKey(
        key=['R_gyr (A^2)'],
        type='target',
        classes=None,
        description='Simulated squared radius of gyration (in Angstroms^2)',
        filter=None,
        units='Angstrom^2'
    )
    foundry_key_5 = FoundryKey(
        key=['Densities (kg/m^3)'],
        type='target',
        classes=None,
        description='Simulated density (in kg/m^3)',
        filter=None,
        units='kg/m^3'
    )
    foundry_schema = FoundrySchema(
        name="test_schema",
        version="1.0",
        data_type='tabular',
        source_id="elwood_md_v1.2",
        domain=["domain"],
        keys=[foundry_key_1, foundry_key_2, foundry_key_3, foundry_key_4, foundry_key_5]
    )
    yield foundry_schema


@pytest.fixture
def mock_hdf5_foundry_schema():
    # foundry_key_1 = FoundryKey(key=["column1", "column2"], type='input')
    # foundry_key_2 = FoundryKey(key=["column2", "column4"], type='output')
    foundry_key_1 = FoundryKey(
        key=['SMILES'],
        type='input',
        classes=None,
        description='Canonical SMILES string of molecule',
        filter=None,
        units='arb'
    )
    foundry_key_2 = FoundryKey(
        key=['E_coh (MPa)'],
        type='target',
        classes=None,
        description='Simulated cohesive energy (in MPa)',
        filter=None,
        units='MPa'
    )
    foundry_key_3 = FoundryKey(
        key=['T_g (K)'],
        type='target',
        classes=None,
        description='Simulated glass transition temperature (in Kelvin)',
        filter=None,
        units='Kelvin'
    )
    foundry_key_4 = FoundryKey(
        key=['R_gyr (A^2)'],
        type='target',
        classes=None,
        description='Simulated squared radius of gyration (in Angstroms^2)',
        filter=None,
        units='Angstrom^2'
    )
    foundry_key_5 = FoundryKey(
        key=['Densities (kg/m^3)'],
        type='target',
        classes=None,
        description='Simulated density (in kg/m^3)',
        filter=None,
        units='kg/m^3'
    )
    foundry_schema = FoundrySchema(
        name="test_schema",
        version="1.0",
        data_type='hdf5',
        source_id="test_dataset",
        domain=["domain"],
        keys=[foundry_key_1, foundry_key_2, foundry_key_3, foundry_key_4, foundry_key_5]
    )
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


def test_load_data_with_globus(mock_foundry_cache, mock_tabular_foundry_schema, mock_read_functions):
    cache = mock_foundry_cache
    foundry_schema = mock_tabular_foundry_schema
    cache._load_data(foundry_schema, file="MD_properties.csv", source_id=foundry_schema.source_id, use_globus=True, as_hdf5=False)
    # Add assertions here


def test_load_data_with_hdf5(mock_foundry_cache, mock_hdf5_foundry_schema, mock_read_functions):
    cache = mock_foundry_cache
    foundry_schema = mock_hdf5_foundry_schema
    cache._load_data(foundry_schema, file="elwood.hdf5", source_id=foundry_schema.source_id, use_globus=False, as_hdf5=True)
    # Add assertions here


def test_load_data_with_globus_2(mock_foundry_cache, mock_tabular_foundry_schema, mock_read_functions):
    cache = mock_foundry_cache
    foundry_schema = mock_tabular_foundry_schema
    cache._load_data(foundry_schema, file="MD_properties.csv", source_id=foundry_schema.source_id, use_globus=True, as_hdf5=False)
    # Add assertions here


def test_load_data_with_source_id(mock_foundry_cache, mock_tabular_foundry_schema, mock_read_functions):
    cache = mock_foundry_cache
    foundry_schema = mock_tabular_foundry_schema
    with pytest.raises(Exception) as exc_info:
        cache._load_data(foundry_schema, file="MD_properties.csv", source_id="12345", use_globus=False, as_hdf5=False)
    err = exc_info.value
    assert isinstance(err, FileNotFoundError)
