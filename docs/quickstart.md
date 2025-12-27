# Quick Start

Load your first materials science dataset in under 5 minutes.

## 1. Install

```bash
pip install foundry-ml
```

## 2. Connect

```python
from foundry import Foundry

f = Foundry()
```

For cloud environments (Colab, remote Jupyter):

```python
f = Foundry(no_browser=True, no_local_server=True)
```

## 3. Search

Find datasets by keyword:

```python
results = f.search("band gap", limit=5)
results
```

Output:
```
                                    dataset_name  ...
0                   foundry_oqmd_band_gaps_v1.1  ...
1                   foundry_aflow_band_gaps_v1.1  ...
2            foundry_experimental_band_gaps_v1.1  ...
...
```

## 4. Load

Get a dataset and load its data:

```python
# Get the first result
dataset = results.iloc[0].FoundryDataset

# Load training data
data = dataset.get_as_dict()
X_train, y_train = data['train']

print(f"Samples: {len(X_train)}")
```

## 5. Understand

Check what fields the dataset contains:

```python
schema = dataset.get_schema()

print(f"Dataset: {schema['name']}")
print(f"Fields:")
for field in schema['fields']:
    print(f"  - {field['name']} ({field['role']})")
```

## 6. Cite

Get the citation for publications:

```python
print(dataset.get_citation())
```

## Complete Example

```python
from foundry import Foundry

# Connect
f = Foundry()

# Search
results = f.search("band gap", limit=5)

# Load
dataset = results.iloc[0].FoundryDataset
X, y = dataset.get_as_dict()['train']

# Use with sklearn
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
# model.fit(X, y)  # Train your model

# Cite
print(dataset.get_citation())
```

## What's Next?

| Task | Guide |
|------|-------|
| Search effectively | [Searching for Datasets](guide/searching.md) |
| Load different formats | [Loading Data](guide/loading-data.md) |
| Use with PyTorch/TensorFlow | [ML Frameworks](guide/ml-frameworks.md) |
| Use from terminal | [CLI](features/cli.md) |
| Publish your data | [Publishing Datasets](publishing/publishing-datasets.md) |
