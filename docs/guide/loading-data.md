# Loading Data

Once you've found a dataset, here's how to load and use it.

## Basic Loading

```python
from foundry import Foundry

f = Foundry()
results = f.search("band gap", limit=1)
dataset = results.iloc[0].FoundryDataset

# Load all data
data = dataset.get_as_dict()
```

## Understanding the Data Structure

Most datasets have this structure:

```python
data = {
    'train': (X_train, y_train),  # Inputs and targets
    'test': (X_test, y_test),
}
```

Access training data:

```python
X_train, y_train = data['train']
```

## Loading Specific Splits

```python
# Load only training data
train_data = dataset.get_as_dict(split='train')

# Load only test data
test_data = dataset.get_as_dict(split='test')
```

## Loading with Schema

Get data and metadata together:

```python
result = dataset.get_as_dict(include_schema=True)

data = result['data']
schema = result['schema']

print(f"Dataset: {schema['name']}")
print(f"Fields: {schema['fields']}")
```

## Data Types

### Tabular Data

Most common format - dictionaries of arrays:

```python
X, y = data['train']

# X might be:
# {'composition': [...], 'structure': [...]}

# y might be:
# {'band_gap': [...]}
```

### Working with DataFrames

```python
import pandas as pd

X, y = data['train']
df = pd.DataFrame(X)
df['target'] = list(y.values())[0]
```

## HDF5 Data

For large datasets, use lazy loading:

```python
data = dataset.get_as_dict(as_hdf5=True)
# Returns h5py objects that load on access
```

## Caching

Data is cached locally after first download:

```python
# First call downloads
data = dataset.get_as_dict()  # Slow

# Subsequent calls use cache
data = dataset.get_as_dict()  # Fast
```

### Custom Cache Location

```python
f = Foundry(local_cache_dir="/path/to/cache")
```

### Clear Cache

```python
f.delete_dataset_cache("dataset_name")
```

## Common Patterns

### Train/Test Split

```python
data = dataset.get_as_dict()

X_train, y_train = data['train']
X_test, y_test = data['test']

# Train model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(pd.DataFrame(X_train), list(y_train.values())[0])
```

### Single Target Column

```python
X, y = data['train']
target_name = list(y.keys())[0]  # Get first target
target_values = y[target_name]
```

### Multiple Inputs

```python
X, y = data['train']

# Combine inputs into DataFrame
import pandas as pd
df = pd.DataFrame(X)
print(df.columns)  # See all input features
```

## Error Handling

```python
from foundry.errors import DownloadError, DataLoadError

try:
    data = dataset.get_as_dict()
except DownloadError as e:
    print(f"Download failed: {e.message}")
    print(f"Try: {e.recovery_hint}")
except DataLoadError as e:
    print(f"Could not load data: {e.message}")
```
