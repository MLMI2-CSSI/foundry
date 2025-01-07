from ..utils import optional_import, require_package

tf = optional_import('tensorflow')

class TensorflowSequence:
    def __init__(self, inputs, targets):
        if not tf:
            require_package('tensorflow', 'TensorflowSequence')
            
        self.inputs = inputs
        self.targets = targets
        
    def __getitem__(self, idx):
        return self.inputs[idx], self.targets[idx]
        
    def __len__(self):
        return len(self.inputs)
