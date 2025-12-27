# Introduction

<p align="center">
  <img src=".gitbook/assets/foundry-purple%20%283%29.png" alt="Foundry" width="400">
</p>

**Foundry-ML** is a Python library that simplifies access to machine learning-ready datasets in materials science and chemistry.

## Features

- **Search & Discover** - Find datasets by keyword or browse the catalog
- **Rich Metadata** - Understand datasets before downloading with detailed schemas
- **Easy Loading** - Get data in Python, PyTorch, or TensorFlow format
- **Automatic Caching** - Fast subsequent access after first download
- **Publishing** - Share your own datasets with the community
- **AI Integration** - MCP server for AI assistant access
- **CLI** - Terminal-based workflows

## Quick Example

```python
from foundry import Foundry

# Connect
f = Foundry()

# Search for datasets
results = f.search("band gap", limit=5)

# Load a dataset
dataset = results.iloc[0].FoundryDataset
X, y = dataset.get_as_dict()['train']

# Get citation for your paper
print(dataset.get_citation())
```

## Installation

```bash
pip install foundry-ml
```

For cloud environments (Colab, remote Jupyter):

```python
f = Foundry(no_browser=True, no_local_server=True)
```

## What's Next?

<table>
<tr>
<td>

**Getting Started**
- [Installation](installation.md)
- [Quick Start](quickstart.md)

</td>
<td>

**User Guide**
- [Searching](guide/searching.md)
- [Loading Data](guide/loading-data.md)
- [ML Frameworks](guide/ml-frameworks.md)

</td>
<td>

**Features**
- [CLI](features/cli.md)
- [MCP Server](features/mcp-server.md)
- [HuggingFace](features/huggingface.md)

</td>
</tr>
</table>

## Project Support

This work was supported by the National Science Foundation under NSF Award Number: 1931306 "Collaborative Research: Framework: Machine Learning Materials Innovation Infrastructure".

Foundry brings together components from:
- [Materials Data Facility (MDF)](https://materialsdatafacility.org)
- [Data and Learning Hub for Science (DLHub)](https://www.dlhub.org)
- [MAST-ML](https://mastmldocs.readthedocs.io/)
