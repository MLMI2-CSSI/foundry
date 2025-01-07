from PIL import Image
import numpy as np
from pathlib import Path
from typing import Tuple, Any, List
import json

from .base import DataLoader

class ImageDataLoader(DataLoader):
    """Loader for image datasets with optional annotations"""
    
    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
    
    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS
        
    def load(self, file_path: Path, schema, split=None) -> Tuple[Any, Any]:
        """Load image data and associated annotations if they exist"""
        # Load image
        img = Image.open(file_path)
        img_array = np.array(img)
        
        # Check for annotation file
        annotation_path = file_path.with_suffix('.json')
        if annotation_path.exists():
            with open(annotation_path) as f:
                annotations = json.load(f)
        else:
            annotations = None
            
        return img_array, annotations
        
    def load_batch(self, file_paths: List[Path], schema, split=None) -> Tuple[Any, Any]:
        """Load multiple images efficiently"""
        images = []
        annotations = []
        
        for path in file_paths:
            img, annot = self.load(path, schema, split)
            images.append(img)
            annotations.append(annot)
            
        return np.stack(images), annotations 