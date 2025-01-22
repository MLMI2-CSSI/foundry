import numpy as np
from pathlib import Path
from typing import Tuple, Any

from .base import DataLoader

class NumpyDataLoader(DataLoader):
    """Loader for NumPy array formats (.npy, .npz)"""
    
    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in {'.npy', '.npz'}
        
    def load(self, file_path: Path, schema, split=None) -> Tuple[Any, Any]:
        if file_path.suffix.lower() == '.npz':
            with np.load(file_path) as data:
                input_keys = self.get_keys(schema, "input")
                target_keys = self.get_keys(schema, "target")
                return (
                    {k: data[k] for k in input_keys},
                    {k: data[k] for k in target_keys}
                )
        else:
            # For .npy files, assume single array split between input/target
            data = np.load(file_path)
            n_inputs = len(self.get_keys(schema, "input"))
            return data[:, :n_inputs], data[:, n_inputs:] 