import pandas as pd
import json
from pathlib import Path

def _read_csv(path_to_file: str, **kwargs):
    """Read a CSV file into a pandas DataFrame"""
    return pd.read_csv(path_to_file, **kwargs)

def _read_json(path_to_file: str, lines: bool = False, **kwargs):
    """Read a JSON file into a pandas DataFrame"""
    if lines:
        return pd.read_json(path_to_file, lines=True, **kwargs)
    return pd.read_json(path_to_file, **kwargs)

def _read_excel(path_to_file: str, **kwargs):
    """Read an Excel file into a pandas DataFrame"""
    return pd.read_excel(path_to_file, **kwargs) 