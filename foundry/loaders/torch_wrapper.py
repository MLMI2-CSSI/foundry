from ..utils import optional_import, require_package

torch = optional_import('torch')

class TorchDataset:
    def __init__(self, inputs, targets):
        if not torch:
            require_package('torch', 'TorchDataset')
            
        self.inputs = inputs
        self.targets = targets
        
    def __getitem__(self, idx):
        return self.inputs[idx], self.targets[idx]
        
    def __len__(self):
        return len(self.inputs)
