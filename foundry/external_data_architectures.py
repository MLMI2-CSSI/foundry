import numpy as np
import torch
from torch.utils.data import Dataset

class FoundryDataset_Torch(Dataset):
    """Foundry Dataset Converted to Pytorch Format"""

    def __init__(self, inputs, targets):
        self.inputs=inputs
        self.targets=targets

    def __len__(self):
        return len(self.inputs[0])

    def __getitem__(self, idx):
        item = {"input": [], "target": []}
        
        for input in self.inputs:
            item["input"].append(np.array(input[idx]))
        item["input"] = np.array(item["input"])
        
        for target in self.targets:
            item["target"].append(np.array(target[idx]))
        item["target"] = np.array(item["target"])
        
        return item
    
