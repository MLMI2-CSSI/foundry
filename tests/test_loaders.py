import pytest
from pathlib import Path
import numpy as np
import pandas as pd
import h5py
import tempfile
import os

from foundry.loaders.base import DataLoader
from foundry.loaders.tabular import TabularDataLoader
from foundry.loaders.hdf5 import HDF5DataLoader
from foundry.loaders.registry import LoaderRegistry
from foundry.models import FoundrySchema

@pytest.fixture
def sample_schema():
    """Create a sample schema for testing"""
    return FoundrySchema({
        'data_type': 'tabular',
        'keys': [
            {'key': ['x1', 'x2'], 'type': 'input'},
            {'key': ['y'], 'type': 'target'}
        ]
    })

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return pd.DataFrame({
        'x1': [1, 2, 3],
        'x2': [4, 5, 6],
        'y': [7, 8, 9]
    })

class TestTabularLoader:
    @pytest.fixture
    def loader(self):
        return TabularDataLoader('./data')

    def test_supports_format(self, loader):
        assert loader.supports_format(Path('data.csv'))
        assert loader.supports_format(Path('data.json'))
        assert loader.supports_format(Path('data.xlsx'))
        assert not loader.supports_format(Path('data.h5'))

    def test_load_csv(self, loader, sample_schema, sample_data, tmp_path):
        # Save sample data
        csv_path = tmp_path / 'test.csv'
        sample_data.to_csv(csv_path, index=False)
        
        # Load and verify
        inputs, targets = loader.load(csv_path, sample_schema)
        assert np.array_equal(inputs['x1'], sample_data['x1'])
        assert np.array_equal(inputs['x2'], sample_data['x2'])
        assert np.array_equal(targets['y'], sample_data['y'])

    def test_load_json(self, loader, sample_schema, sample_data, tmp_path):
        # Save sample data
        json_path = tmp_path / 'test.json'
        sample_data.to_json(json_path)
        
        # Load and verify
        inputs, targets = loader.load(json_path, sample_schema)
        assert np.array_equal(inputs['x1'], sample_data['x1'])
        assert np.array_equal(inputs['x2'], sample_data['x2'])
        assert np.array_equal(targets['y'], sample_data['y'])

    def test_invalid_format(self, loader, sample_schema):
        with pytest.raises(ValueError):
            loader.load(Path('nonexistent.txt'), sample_schema)

class TestHDF5Loader:
    @pytest.fixture
    def loader(self):
        return HDF5DataLoader('./data')

    def test_supports_format(self, loader):
        assert loader.supports_format(Path('data.h5'))
        assert loader.supports_format(Path('data.hdf5'))
        assert not loader.supports_format(Path('data.csv'))

    def test_load_hdf5(self, loader, sample_schema, tmp_path):
        # Create sample HDF5 file
        h5_path = tmp_path / 'test.h5'
        with h5py.File(h5_path, 'w') as f:
            f.create_dataset('x1', data=[1, 2, 3])
            f.create_dataset('x2', data=[4, 5, 6])
            f.create_dataset('y', data=[7, 8, 9])
        
        # Test normal loading
        inputs, targets = loader.load(h5_path, sample_schema)
        assert np.array_equal(inputs['x1'], [1, 2, 3])
        assert np.array_equal(inputs['x2'], [4, 5, 6])
        assert np.array_equal(targets['y'], [7, 8, 9])

    def test_load_hdf5_as_hdf5(self, loader, sample_schema, tmp_path):
        # Create sample HDF5 file
        h5_path = tmp_path / 'test.h5'
        with h5py.File(h5_path, 'w') as f:
            f.create_dataset('x1', data=[1, 2, 3])
            f.create_dataset('x2', data=[4, 5, 6])
            f.create_dataset('y', data=[7, 8, 9])
        
        # Test loading with as_hdf5=True
        inputs, targets = loader.load(h5_path, sample_schema, as_hdf5=True)
        assert isinstance(inputs['x1'], h5py.Dataset)
        assert isinstance(inputs['x2'], h5py.Dataset)
        assert isinstance(targets['y'], h5py.Dataset)

class TestLoaderRegistry:
    @pytest.fixture
    def registry(self):
        return LoaderRegistry()

    def test_get_loader_by_type(self, registry):
        loader = registry.get_loader(Path('data.csv'), 'tabular', './data')
        assert isinstance(loader, TabularDataLoader)

    def test_get_loader_by_extension(self, registry):
        loader = registry.get_loader(Path('data.h5'), None, './data')
        assert isinstance(loader, HDF5DataLoader)

    def test_no_suitable_loader(self, registry):
        with pytest.raises(ValueError):
            registry.get_loader(Path('data.unknown'), None, './data')

    def test_register_custom_loader(self, registry):
        class CustomLoader(DataLoader):
            def supports_format(self, file_path):
                return file_path.suffix == '.custom'
            def load(self, file_path, schema, split=None, as_hdf5=False):
                return None, None

        registry.register_loader('custom', CustomLoader)
        loader = registry.get_loader(Path('data.custom'), 'custom', './data')
        assert isinstance(loader, CustomLoader)

@pytest.mark.integration
class TestIntegration:
    def test_end_to_end_tabular(self, tmp_path):
        # Create test data
        df = pd.DataFrame({
            'x1': [1, 2, 3],
            'x2': [4, 5, 6],
            'y': [7, 8, 9]
        })
        csv_path = tmp_path / 'test.csv'
        df.to_csv(csv_path, index=False)

        # Create schema
        schema = FoundrySchema({
            'data_type': 'tabular',
            'keys': [
                {'key': ['x1', 'x2'], 'type': 'input'},
                {'key': ['y'], 'type': 'target'}
            ]
        })

        # Test loading through registry
        registry = LoaderRegistry()
        loader = registry.get_loader(csv_path, schema.data_type, str(tmp_path))
        inputs, targets = loader.load(csv_path, schema)

        assert np.array_equal(inputs['x1'], df['x1'])
        assert np.array_equal(inputs['x2'], df['x2'])
        assert np.array_equal(targets['y'], df['y']) 