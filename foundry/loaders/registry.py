from pathlib import Path
from typing import Dict, Type

from ..utils import optional_import

from .base import DataLoader
from .tabular import TabularDataLoader
from .hdf5 import HDF5DataLoader
from .numpy import NumpyDataLoader
from .image import ImageDataLoader

class LoaderRegistry:
    """Registry for managing available data loaders"""
    
    def __init__(self):
        self._loaders: Dict[str, Type[DataLoader]] = {}
        
        # Always register core loaders
        self.register_loader("tabular", TabularDataLoader)
        self.register_loader("hdf5", HDF5DataLoader)
        self.register_loader("numpy", NumpyDataLoader)
        self.register_loader("image", ImageDataLoader)
        
        # Conditionally register optional loaders
        if optional_import('rdkit'):
            from .molecular import MolecularDataLoader
            self.register_loader("molecular", MolecularDataLoader)
            
        if optional_import('jcamp'):
            from .spectral import SpectralDataLoader
            self.register_loader("spectral", SpectralDataLoader)
        
    def register_loader(self, name: str, loader_class: Type[DataLoader]):
        """Register a new loader class"""
        self._loaders[name] = loader_class
        
    def get_loader(self, file_path: Path, schema_type: str, cache_dir: str) -> DataLoader:
        """Get appropriate loader instance for file"""
        if schema_type in self._loaders:
            return self._loaders[schema_type](cache_dir)
            
        # Try to find loader that supports the format
        for loader_class in self._loaders.values():
            loader = loader_class(cache_dir)
            if loader.supports_format(file_path):
                return loader
                
        raise ValueError(f"No suitable loader found for {file_path}") 