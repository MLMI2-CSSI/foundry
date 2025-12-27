# Installation

## Requirements

- Python 3.8 or higher
- pip package manager

## Basic Installation

Install Foundry-ML from PyPI:

```bash
pip install foundry-ml
```

This installs the core package with HTTPS download support. No additional setup required.

## Optional Dependencies

### HuggingFace Integration

To export datasets to HuggingFace Hub:

```bash
pip install foundry-ml[huggingface]
```

### All Optional Dependencies

```bash
pip install foundry-ml[all]
```

## Verify Installation

```python
from foundry import Foundry

f = Foundry()
print("Foundry installed successfully!")

# Test search
results = f.search("band gap", limit=1)
print(f"Found {len(results)} datasets")
```

## Cloud Environments

### Google Colab

Foundry works in Colab without additional setup:

```python
!pip install foundry-ml

from foundry import Foundry
f = Foundry(no_browser=True, no_local_server=True)
```

### Jupyter Notebooks

For Jupyter running on remote servers:

```python
from foundry import Foundry
f = Foundry(no_browser=True, no_local_server=True)
```

## Globus Setup (Optional)

For large dataset transfers, you can use Globus instead of HTTPS:

1. Install [Globus Connect Personal](https://www.globus.org/globus-connect-personal)
2. Start the Globus endpoint
3. Enable Globus in Foundry:

```python
f = Foundry(use_globus=True)
```

**Note:** HTTPS is the default and works for most use cases. Only use Globus if you're transferring very large datasets (>10GB) or have institutional Globus endpoints.

## Troubleshooting

### Import Errors

If you get import errors, ensure you have the latest version:

```bash
pip install --upgrade foundry-ml
```

### Network Issues

Foundry requires internet access to search and download datasets. If behind a proxy:

```python
import os
os.environ['HTTP_PROXY'] = 'http://proxy:port'
os.environ['HTTPS_PROXY'] = 'http://proxy:port'

from foundry import Foundry
f = Foundry()
```

### Cache Location

By default, datasets are cached in your home directory. To change:

```python
f = Foundry(local_cache_dir="/path/to/cache")
```

## Next Steps

- [Quick Start](quickstart.md) - Load your first dataset
- [CLI](features/cli.md) - Use Foundry from the command line
