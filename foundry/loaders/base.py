from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, Optional
from pathlib import Path

from foundry.jsonschema_models.project_model import Split
from foundry.models import FoundrySchema

class DataLoader(ABC):
    """Base class for all Foundry data loaders"""
    
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
    
    @abstractmethod
    def load(self, 
             file_path: Path,
             schema: FoundrySchema,
             split: Optional[Split] = None,
             as_hdf5: bool = False) -> Tuple[Any, Any]:
        """Load data from file and return input/target tuple"""
        pass
    
    @abstractmethod
    def supports_format(self, file_path: Path) -> bool:
        """Check if this loader supports the given file format"""
        pass
        
    def get_keys(self, schema: FoundrySchema, key_type: str) -> list:
        """Extract keys of given type from schema"""
        keys = [key.key for key in schema.keys if key.type == key_type]
        return [k for sublist in keys for k in sublist]  # Flatten 