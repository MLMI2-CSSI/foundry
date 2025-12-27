# Hello Foundry!

This is the **beginner-friendly** example for Foundry-ML.

No domain expertise required - just Python basics.

## What You'll Learn

1. How to connect to Foundry
2. How to search for datasets
3. How to load data into Python
4. How to explore dataset schemas
5. How to get proper citations

## Quick Start

```python
from foundry import Foundry

# Connect
f = Foundry()

# Search
results = f.search("band gap", limit=5)

# Load
dataset = results.iloc[0].FoundryDataset
data = dataset.get_as_dict()

# Use
X, y = data['train']
```

## Running in Google Colab

For cloud environments, use:

```python
f = Foundry(no_browser=True, no_local_server=True)
```

## Next Steps

After this example, check out:
- `/examples/bandgap/` - Working with band gap datasets
- `/examples/publishing/` - How to publish your own datasets

## Need Help?

- Documentation: https://github.com/MLMI2-CSSI/foundry
- CLI help: `foundry --help`
