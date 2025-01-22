import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from foundry.utils.io import _read_csv, _read_json, _read_excel
from foundry.utils.validation import is_doi, is_pandas_pytable
from foundry.utils.imports import optional_import, require_package

def test_read_csv(tmp_path):
    # Create test CSV
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    path = tmp_path / 'test.csv'
    df.to_csv(path, index=False)
    
    result = _read_csv(str(path))
    pd.testing.assert_frame_equal(result, df)

def test_read_json(tmp_path):
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    path = tmp_path / 'test.json'
    df.to_json(path)
    
    result = _read_json(str(path))
    pd.testing.assert_frame_equal(result, df)

def test_read_excel(tmp_path):
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    path = tmp_path / 'test.xlsx'
    df.to_excel(path, index=False)
    
    result = _read_excel(str(path))
    pd.testing.assert_frame_equal(result, df)

def test_is_doi():
    assert is_doi('10.1234/abc123')
    assert not is_doi('not-a-doi')

def test_optional_import():
    np = optional_import('numpy')
    assert np is not None
    
    nonexistent = optional_import('nonexistent_package')
    assert nonexistent is None

def test_require_package():
    with pytest.raises(ImportError) as exc:
        require_package('test_package', 'TestFeature')
    assert 'TestFeature requires test_package' in str(exc.value) 