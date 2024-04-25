from pathlib import Path
import pytest

from foundry import foundry
from tests.test_data import datacite_data, valid_metadata


def test_dataset_instantiation():
    ds = foundry.FoundryDataset(dataset_name='peanuts',
                                foundry_schema=valid_metadata,
                                datacite_entry=datacite_data)

    assert ds.foundry_schema is not None


def test_dataset_instantiation_broken_dc():
    broken_datacite = datacite_data.copy()
    broken_datacite.pop('creators')
    with pytest.raises(Exception) as exc_info:
        foundry.FoundryDataset(dataset_name='peanuts',
                               foundry_schema=valid_metadata,
                               datacite_entry=broken_datacite)
        print(f'ERROR: {exc_info.value}')
        assert "field required" in str(exc_info.value)


def test_add_non_existent_data_to_dataset():
    ds = foundry.FoundryDataset(dataset_name='peanuts',
                                foundry_schema=valid_metadata,
                                datacite_entry=datacite_data)

    with pytest.raises(ValueError) as exc_info:
        ds.add_data(local_data_path='./test_data/iris.csv')
        print(f'ERROR: {exc_info.value}')
        assert "local path" in str(exc_info.value)


def test_add_data_folder_to_dataset():
    ds = foundry.FoundryDataset(dataset_name='peanuts',
                                foundry_schema=valid_metadata,
                                datacite_entry=datacite_data)
    dir_path = str(Path(__file__).parent) + '/test_data/test_dataset'
    ds.add_data(local_data_path=dir_path)
    assert hasattr(ds, '_local_data_path')


def test_add_data_file_to_dataset():
    ds = foundry.FoundryDataset(dataset_name='peanuts',
                                foundry_schema=valid_metadata,
                                datacite_entry=datacite_data)
    file_path = str(Path(__file__).parent) + '/test_data/test_dataset/elwood.hdf5'
    ds.add_data(local_data_path=file_path)
    assert hasattr(ds, '_local_data_path')
