# Frequently Asked Questions

## General

### What is Foundry?

Foundry-ML is a Python library for discovering and loading machine learning-ready datasets in materials science and chemistry. It provides standardized access to curated scientific datasets with rich metadata.

### Is Foundry free?

Yes. Foundry is open source and the datasets are freely available. Some datasets may have specific licenses - check the citation information for details.

### Do I need to create an account?

No account is required for basic usage with HTTPS download. Some features (like Globus transfers) may require authentication.

## Installation

### What Python version do I need?

Python 3.8 or higher.

### How do I install Foundry?

```bash
pip install foundry-ml
```

### I get import errors after installing

Try upgrading:

```bash
pip install --upgrade foundry-ml
```

## Data Loading

### Why is my first download slow?

Data is downloaded on first access and cached locally. Subsequent loads are fast.

### Where is data cached?

By default, in your home directory. To change:

```python
f = Foundry(local_cache_dir="/path/to/cache")
```

### How do I clear the cache?

```python
f.delete_dataset_cache("dataset_name")
```

### Can I use Foundry offline?

You need internet to search and download datasets. Once cached, data loads locally.

## Cloud Environments

### How do I use Foundry in Google Colab?

```python
!pip install foundry-ml

from foundry import Foundry
f = Foundry(no_browser=True, no_local_server=True)
```

### Does it work with Jupyter on a remote server?

Yes, use the same settings:

```python
f = Foundry(no_browser=True, no_local_server=True)
```

## Data Format

### What format is the data in?

Most datasets use a dictionary format:

```python
data = {
    'train': (X_dict, y_dict),
    'test': (X_dict, y_dict)
}
```

### How do I get a pandas DataFrame?

```python
import pandas as pd

X, y = data['train']
df = pd.DataFrame(X)
```

### Does it work with PyTorch?

Yes:

```python
torch_dataset = dataset.get_as_torch(split='train')
```

### Does it work with TensorFlow?

Yes:

```python
tf_dataset = dataset.get_as_tensorflow(split='train')
```

## Publishing

### How do I publish my own dataset?

See [Publishing Datasets](../publishing/publishing-datasets.md) for the full workflow.

### What metadata format is required?

Foundry uses DataCite-compliant metadata. See [Metadata Reference](../publishing/metadata-reference.md).

### Can I update a published dataset?

Create a new version with an updated source_id (e.g., `my_dataset_v2`).

## Globus

### Do I need Globus?

No. HTTPS download is the default and works for most use cases.

### When should I use Globus?

For very large datasets (>10GB) or if you have institutional Globus endpoints.

### How do I enable Globus?

```python
f = Foundry(use_globus=True)
```

You'll need [Globus Connect Personal](https://www.globus.org/globus-connect-personal) running.

## AI Integration

### How do I use Foundry with Claude?

Install the MCP server:

```bash
foundry mcp install
```

Restart Claude Code. You can now ask Claude to find and load datasets.

### What AI assistants are supported?

Any MCP-compatible assistant. Currently tested with Claude Code.

## HuggingFace

### Can I export to HuggingFace Hub?

Yes:

```bash
pip install foundry-ml[huggingface]
foundry push-to-hf 10.18126/abc123 --repo your-username/dataset-name
```

### Who is listed as author on HuggingFace?

The original dataset creators from the DataCite metadata, not the person pushing.

## Troubleshooting

### I get "Dataset not found"

Check:
1. The DOI is correct
2. Try a broader search term
3. List available datasets: `f.list()`

### Download keeps failing

Try:
1. Check your internet connection
2. Try again (transient errors)
3. If using Globus, switch to HTTPS: `f = Foundry(use_globus=False)`

### The data format is unexpected

Check the schema first:

```python
schema = dataset.get_schema()
print(schema['fields'])
print(schema['splits'])
```

## More Help

- [Documentation](https://ai-materials-and-chemistry.gitbook.io/foundry/)
- [GitHub Issues](https://github.com/MLMI2-CSSI/foundry/issues)
- [Troubleshooting](troubleshooting.md)
