import pytest
import numpy as np
from pathlib import Path

from foundry.utils import optional_import
from foundry.models import FoundrySchema

# Import optional dependencies
torch = optional_import('torch')
tf = optional_import('tensorflow')
rdkit = optional_import('rdkit')

# Only import loaders if dependencies are available
if torch:
    from foundry.loaders.torch_wrapper import TorchDataset
if tf:
    from foundry.loaders.tf_wrapper import TensorflowSequence
if rdkit:
    from foundry.loaders.molecular import MolecularDataLoader
    from rdkit import Chem

@pytest.fixture
def sample_data():
    return {
        'inputs': np.array([[1, 2], [3, 4]]),
        'targets': np.array([5, 6])
    }

@pytest.mark.skipif(not torch, reason="PyTorch not installed")
def test_torch_dataset(sample_data):
    dataset = TorchDataset(sample_data['inputs'], sample_data['targets'])
    assert len(dataset) == 2
    inputs, targets = dataset[0]
    assert np.array_equal(inputs, [1, 2])
    assert targets == 5

@pytest.mark.skipif(not tf, reason="TensorFlow not installed")
def test_tensorflow_sequence(sample_data):
    sequence = TensorflowSequence(sample_data['inputs'], sample_data['targets'])
    assert len(sequence) == 2
    inputs, targets = sequence[0]
    assert np.array_equal(inputs, [1, 2])
    assert targets == 5

@pytest.mark.skipif(not rdkit, reason="RDKit not installed")
class TestMolecularLoader:
    @pytest.fixture
    def loader(self):
        return MolecularDataLoader('./data')

    def test_supports_format(self, loader):
        assert loader.supports_format(Path('test.sdf'))
        assert loader.supports_format(Path('test.mol2'))
        assert not loader.supports_format(Path('test.csv'))

    def test_load_sdf(self, loader, tmp_path):
        sdf_path = tmp_path / 'test.sdf'
        with open(sdf_path, 'w') as f:
            f.write("""
            Test molecule
                RDKit          3D
                
              0  0  0  0  0  0  0  0  0  0999 V2000
                0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
            M  END
            $$$$
            """)
        
        schema = FoundrySchema({
            'data_type': 'molecular',
            'keys': [
                {'key': ['morgan_fp'], 'type': 'input'},
                {'key': ['molecular_weight'], 'type': 'target'}
            ]
        })
        
        inputs, targets = loader.load(sdf_path, schema)
        assert 'morgan_fp' in inputs
        assert 'molecular_weight' in targets 