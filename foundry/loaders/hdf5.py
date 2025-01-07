import h5py
from pathlib import Path
from typing import Tuple, Any

from .base import DataLoader
from ..utils import is_pandas_pytable

class HDF5DataLoader(DataLoader):
    """Loader for HDF5 data formats"""
    
    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in {'.h5', '.hdf5'}
        
    def load(self, file_path: Path, schema, split=None, as_hdf5: bool = False) -> Tuple[Any, Any]:
        """Load HDF5 data
        
        Args:
            file_path: Path to HDF5 file
            schema: Schema describing the data format
            split: Optional split information
            as_hdf5: If True, return h5py Dataset objects instead of converting to arrays
            
        Returns:
            Tuple of (input_data, target_data)
        """
        with h5py.File(str(file_path), 'r') as f:
            input_keys = self.get_keys(schema, "input")
            target_keys = self.get_keys(schema, "target")
            
            if as_hdf5:
                inputs = {k: f[k] for k in input_keys}
                targets = {k: f[k] for k in target_keys}
            else:
                inputs = {k: f[k][:] for k in input_keys}
                targets = {k: f[k][:] for k in target_keys}
                
            return inputs, targets 