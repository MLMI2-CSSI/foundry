import pytest
from pathlib import Path
import pandas as pd

from foundry.loaders.base import DataLoader
from foundry.loaders.registry import LoaderRegistry
from foundry.models import FoundrySchema

def test_loader_not_found():
    registry = LoaderRegistry()
    with pytest.raises(ValueError, match="No suitable loader found"):
        registry.get_loader(Path('test.xyz'), None, './data')

def test_missing_file():
    class TestLoader(DataLoader):
        def __init__(self, cache_dir):
            super().__init__(cache_dir)
            
        def supports_format(self, file_path):
            return True
            
        def load(self, file_path, schema, split=None, as_hdf5=False):
            if not file_path.exists():
                raise FileNotFoundError(f"No file found at: {file_path}")
            return None, None
            
    loader = TestLoader('./data')
    with pytest.raises(FileNotFoundError):
        loader.load(Path('nonexistent.txt'), FoundrySchema({}))

@pytest.fixture
def test_csv(tmp_path):
    # Create test CSV file
    csv_path = tmp_path / 'test.csv'
    df = pd.DataFrame({
        'col1': [1, 2],
        'col2': [3, 4]
    })
    df.to_csv(csv_path, index=False)
    return csv_path

def test_missing_schema_keys(test_csv):
    registry = LoaderRegistry()
    schema = FoundrySchema({
        'data_type': 'tabular',
        'keys': []  # Empty keys
    })
    
    loader = registry.get_loader(test_csv, schema.data_type, './data')
    with pytest.raises(ValueError, match="No keys defined"):
        loader.load(test_csv, schema)

def test_invalid_key_type(test_csv):
    registry = LoaderRegistry()
    schema = FoundrySchema({
        'data_type': 'tabular',
        'keys': [
            {'key': ['col1'], 'type': 'invalid_type'}  # Invalid key type
        ]
    })
    
    loader = registry.get_loader(test_csv, schema.data_type, './data')
    with pytest.raises(ValueError, match="Invalid key type"):
        loader.load(test_csv, schema)

def test_unsupported_format():
    class TestLoader(DataLoader):
        def __init__(self, cache_dir):
            super().__init__(cache_dir)
            
        def supports_format(self, file_path):
            return file_path.suffix == '.test'
            
        def load(self, file_path, schema, split=None, as_hdf5=False):
            if not self.supports_format(file_path):
                raise ValueError(f"Unsupported format: {file_path.suffix}")
            return None, None
            
    loader = TestLoader('./data')
    with pytest.raises(ValueError, match="Unsupported format"):
        loader.load(Path('test.txt'), FoundrySchema({})) 