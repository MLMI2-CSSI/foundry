# Dataset Schemas

Schemas describe what data a dataset contains, helping you understand before you load.

## Getting the Schema

```python
from foundry import Foundry

f = Foundry()
dataset = f.search("band gap", limit=1).iloc[0].FoundryDataset

schema = dataset.get_schema()
```

## Schema Structure

```python
{
    'name': 'foundry_oqmd_band_gaps_v1.1',
    'title': 'OQMD Band Gaps Dataset',
    'doi': '10.18126/abc123',
    'description': 'Band gaps calculated using DFT...',
    'data_type': 'tabular',
    'fields': [...],
    'splits': [...]
}
```

## Fields

Fields describe each column/feature in the dataset:

```python
for field in schema['fields']:
    print(f"Name: {field['name']}")
    print(f"Role: {field['role']}")  # 'input' or 'target'
    print(f"Description: {field['description']}")
    print(f"Units: {field['units']}")
    print("---")
```

Example output:
```
Name: composition
Role: input
Description: Chemical composition formula
Units: None
---
Name: band_gap
Role: target
Description: DFT-calculated band gap
Units: eV
---
```

## Splits

Splits show how data is divided:

```python
for split in schema['splits']:
    print(f"{split['name']}: {split.get('type', 'data')}")
```

Example output:
```
train: train
test: test
```

## Data Types

The `data_type` field indicates the format:

| Type | Description |
|------|-------------|
| `tabular` | Rows and columns (most common) |
| `hierarchical` | Nested/tree structure |
| `image` | Image data |

## Using Schema Information

### Filter by Field Role

```python
input_fields = [f for f in schema['fields'] if f['role'] == 'input']
target_fields = [f for f in schema['fields'] if f['role'] == 'target']

print(f"Inputs: {[f['name'] for f in input_fields]}")
print(f"Targets: {[f['name'] for f in target_fields]}")
```

### Check Units

```python
for field in schema['fields']:
    if field['units']:
        print(f"{field['name']}: {field['units']}")
```

### Include Schema with Data

```python
result = dataset.get_as_dict(include_schema=True)

data = result['data']
schema = result['schema']

# Now you have both together
X, y = data['train']
print(f"Loading {schema['name']}...")
```

## CLI Schema

```bash
foundry schema 10.18126/abc123
```

Output:
```
Dataset: foundry_oqmd_band_gaps_v1.1
Title: OQMD Band Gaps Dataset
DOI: 10.18126/abc123
Data Type: tabular

Fields:
  [input ] composition: Chemical composition formula
  [target] band_gap: DFT-calculated band gap (eV)

Splits:
  - train
  - test
```

## Best Practices

### Always Check Schema First

```python
# Before loading (no download)
schema = dataset.get_schema()
print(f"Fields: {len(schema['fields'])}")
print(f"Splits: {[s['name'] for s in schema['splits']]}")

# If it looks right, load
data = dataset.get_as_dict()
```

### Validate Data Against Schema

```python
schema = dataset.get_schema()
data = dataset.get_as_dict()

X, y = data['train']

input_names = [f['name'] for f in schema['fields'] if f['role'] == 'input']
for name in input_names:
    if name not in X:
        print(f"Warning: {name} not in data")
```

### Document Your Usage

```python
schema = dataset.get_schema()
print(f"""
Using dataset: {schema['name']}
DOI: {schema['doi']}

Features used:
{chr(10).join(f"- {f['name']}: {f['description']}" for f in schema['fields'] if f['role'] == 'input')}

Target:
{chr(10).join(f"- {f['name']}: {f['description']}" for f in schema['fields'] if f['role'] == 'target')}
""")
```
