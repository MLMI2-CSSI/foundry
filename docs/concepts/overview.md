# Overview

Foundry-ML is a Python library that simplifies access to machine learning-ready datasets in materials science and chemistry. It provides a unified interface to discover, load, and use curated scientific datasets.

## What is Foundry?

Foundry serves as a bridge between data producers (researchers who create datasets) and data consumers (researchers who use datasets for ML). It standardizes how datasets are:

- **Discovered** - Search by keyword, browse catalogs, or get by DOI
- **Described** - Rich metadata including field descriptions, units, and citations
- **Delivered** - Automatic download, caching, and format conversion

## Key Features

### For Data Users

```python
from foundry import Foundry

# Connect and search
f = Foundry()
results = f.search("band gap", limit=5)

# Load a dataset
dataset = results.iloc[0].FoundryDataset
X, y = dataset.get_as_dict()['train']

# Understand the data
schema = dataset.get_schema()
print(schema['fields'])  # What columns exist and what they mean
```

### For AI Agents

Foundry includes an MCP (Model Context Protocol) server that enables AI assistants like Claude to discover and use datasets programmatically:

```bash
foundry mcp install  # Add to Claude Code
```

### For Data Publishers

Share your datasets with the community using standardized metadata:

```python
f.publish(metadata, data_path="./my_data", source_id="my_dataset_v1")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Your Code                            │
├─────────────────────────────────────────────────────────────┤
│                     Foundry Python API                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Search  │  │   Load   │  │  Schema  │  │  Publish │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
├─────────────────────────────────────────────────────────────┤
│                      Data Transport                         │
│         HTTPS (default)  │  Globus (large files)           │
├─────────────────────────────────────────────────────────────┤
│                   Materials Data Facility                   │
│              (Storage, Metadata, DOI Registration)          │
└─────────────────────────────────────────────────────────────┘
```

## Core Concepts

### Datasets

A Foundry dataset contains:
- **Data files** - The actual data (JSON, CSV, HDF5, etc.)
- **Schema** - Description of fields, types, and splits
- **Metadata** - DataCite-compliant citation information

### Splits

Datasets are organized into splits (e.g., `train`, `test`, `validation`) with input/target pairs:

```python
data = dataset.get_as_dict()
X_train, y_train = data['train']
X_test, y_test = data['test']
```

### Keys (Fields)

Each field in a dataset has:
- **Name** - The column/field identifier
- **Type** - `input` or `target`
- **Description** - What the field represents
- **Units** - Physical units (if applicable)

## Ecosystem Integration

Foundry integrates with the broader ML ecosystem:

| Integration | Purpose |
|-------------|---------|
| **PyTorch** | `dataset.get_as_torch()` |
| **TensorFlow** | `dataset.get_as_tensorflow()` |
| **HuggingFace Hub** | Export datasets for broader visibility |
| **MCP Server** | AI agent access |
| **CLI** | Terminal-based workflows |

## Next Steps

- [Installation](../installation.md) - Get Foundry installed
- [Quick Start](../quickstart.md) - Load your first dataset in 5 minutes
- [Searching for Datasets](../guide/searching.md) - Find the right data
