import numpy as np
from torch.utils.data import Dataset


class TorchDataset(Dataset):
    """Foundry Dataset Converted to Pytorch Format"""

    def __init__(self, inputs, targets):
        self.inputs = inputs
        self.targets = targets

    def __len__(self):
        return len(self.inputs[0])

    def __getitem__(self, idx):
        item = {"input": [], "target": []}

        # adds the correct item at index idx from each input from self.inputs to the item dictionary
        for input in self.inputs:
            item["input"].append(np.array(input[idx]))
        item["input"] = np.array(item["input"])

        # adds the correct item at index idx from each target from self.targets to the item dictionary
        for target in self.targets:
            item["target"].append(np.array(target[idx]))
        item["target"] = np.array(item["target"])

        return item
