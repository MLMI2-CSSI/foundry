from pathlib import Path
from typing import Tuple, Any, Dict
import pandas as pd
import numpy as np

from .base import DataLoader
from ..utils import optional_import, require_package

# Lazy import of rdkit
rdkit = optional_import('rdkit')
if rdkit:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors

class MolecularDataLoader(DataLoader):
    """Loader for molecular data formats (.sdf, .mol2, .pdb)"""
    
    SUPPORTED_EXTENSIONS = {'.sdf', '.mol2', '.pdb', '.xyz'}
    
    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS
        
    def load(self, file_path: Path, schema, split=None, as_hdf5: bool = False) -> Tuple[Any, Any]:
        if not rdkit:
            require_package('molecular', 'MolecularDataLoader')
            
        ext = file_path.suffix.lower()
        
        if ext == '.sdf':
            mols = list(Chem.SDMolSupplier(str(file_path)))
        elif ext == '.mol2':
            mols = [Chem.MolFromMol2File(str(file_path))]
        elif ext == '.pdb':
            mols = [Chem.MolFromPDBFile(str(file_path))]
        else:
            raise ValueError(f"Unsupported format: {ext}")
            
        # Convert molecules to features
        features = []
        for mol in mols:
            if mol is not None:
                feat = self._extract_features(mol)
                features.append(feat)
                
        features_array = np.array(features)
        
        # Look for properties file with target values
        props_path = file_path.with_suffix('.csv')
        if props_path.exists():
            props_df = pd.read_csv(props_path)
            targets = props_df[self.get_keys(schema, "target")].values
        else:
            targets = None
            
        return features_array, targets
        
    def _extract_features(self, mol) -> Dict:
        """Extract relevant molecular features"""
        return {
            'morgan_fp': AllChem.GetMorganFingerprintAsBitVect(mol, 2),
            'num_atoms': mol.GetNumAtoms(),
            'num_bonds': mol.GetNumBonds(),
            'molecular_weight': Descriptors.ExactMolWt(mol),
            'logp': Descriptors.MolLogP(mol),
            'polar_surface_area': Descriptors.TPSA(mol)
        } 