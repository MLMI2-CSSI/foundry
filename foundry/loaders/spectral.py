import numpy as np
from pathlib import Path
from typing import Tuple, Any
import pandas as pd
from scipy.io import loadmat

from .base import DataLoader

class SpectralDataLoader(DataLoader):
    """Loader for spectroscopic data formats"""
    
    SUPPORTED_EXTENSIONS = {'.txt', '.csv', '.mat', '.jdx', '.dx'}
    
    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS
        
    def load(self, file_path: Path, schema, split=None) -> Tuple[Any, Any]:
        ext = file_path.suffix.lower()
        
        if ext in {'.txt', '.csv'}:
            # Assume standard format with wavelength/frequency in first column
            data = pd.read_csv(file_path, delimiter=None, engine='python')
            x_values = data.iloc[:, 0].values
            spectra = data.iloc[:, 1:].values
            
        elif ext == '.mat':
            # MATLAB format
            data = loadmat(file_path)
            # Assume standard variable names, could be made configurable
            x_values = data.get('wavelength', data.get('frequency', None))
            spectra = data.get('spectra', None)
            
        elif ext in {'.jdx', '.dx'}:
            # JCAMP-DX format
            try:
                import jcamp  # Optional dependency
                data = jcamp.JCAMP_reader(str(file_path))
                x_values = data['x']
                spectra = data['y']
            except ImportError:
                raise ImportError("jcamp-dx package required for .jdx/.dx files")
                
        else:
            raise ValueError(f"Unsupported format: {ext}")
            
        # Package the spectral data
        input_data = {
            'x_values': x_values,
            'spectra': spectra
        }
        
        # Look for metadata/target values
        meta_path = file_path.with_suffix('.json')
        if meta_path.exists():
            import json
            with open(meta_path) as f:
                target_data = json.load(f)
        else:
            target_data = None
            
        return input_data, target_data 