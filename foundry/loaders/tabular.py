import pandas as pd
from pathlib import Path
from typing import Tuple, Any

from .base import DataLoader
from foundry.utils import _read_csv, _read_json, _read_excel

class TabularDataLoader(DataLoader):
    """Loader for tabular data formats (CSV, JSON, Excel)"""
    
    SUPPORTED_EXTENSIONS = {'.csv', '.json', '.xlsx', '.xls'}
    VALID_KEY_TYPES = {'input', 'target', 'output'}
    
    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS
        
    def load(self, file_path: Path, schema, split=None, as_hdf5: bool = False) -> Tuple[Any, Any]:
        """Load tabular data and split into input/target
        
        Args:
            file_path: Path to data file
            schema: Schema describing the data format
            split: Optional split information 
            as_hdf5: Ignored for tabular data
            
        Returns:
            Tuple of (input_data, target_data)
        """
        # Validate schema
        if not schema.keys:
            raise ValueError("No keys defined in schema")
            
        # Validate key types
        for key in schema.keys:
            if key.type not in self.VALID_KEY_TYPES:
                raise ValueError(f"Invalid key type: {key.type}. Must be one of {self.VALID_KEY_TYPES}")
        
        # Load the data based on file type
        ext = file_path.suffix.lower()
        if ext == '.csv':
            df = _read_csv(str(file_path))
        elif ext == '.json':
            df = _read_json(str(file_path))
        elif ext in {'.xlsx', '.xls'}:
            df = _read_excel(str(file_path))
        else:
            raise ValueError(f"Unsupported format: {ext}")
            
        # Split into input and target features
        input_cols = self.get_keys(schema, "input")
        target_cols = self.get_keys(schema, "target") or self.get_keys(schema, "output")
        
        if not input_cols and not target_cols:
            raise ValueError("No input or target keys found in schema")
            
        return df[input_cols], df[target_cols] 