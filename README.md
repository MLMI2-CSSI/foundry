
<picture>
  <source srcset="https://raw.githubusercontent.com/MLMI2-CSSI/foundry/main/assets/foundry-white.png" height=175" media="(prefers-color-scheme: dark)">
  <img src="https://raw.githubusercontent.com/MLMI2-CSSI/foundry/main/assets/foundry-black.png" height="175">
</picture>

[![PyPI](https://img.shields.io/pypi/v/foundry_ml.svg)](https://pypi.python.org/pypi/foundry_ml)
[![Tests](https://github.com/MLMI2-CSSI/foundry/actions/workflows/tests.yml/badge.svg)](https://github.com/MLMI2-CSSI/foundry/actions/workflows/tests.yml)
[![NSF-1931306](https://img.shields.io/badge/NSF-1931306-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1931306&HistoricalAwards=false)
[<img src="https://img.shields.io/badge/view-documentation-blue">](https://ai-materials-and-chemistry.gitbook.io/foundry/)

**Foundry-ML** simplifies access to machine learning-ready datasets in materials science and chemistry.

- **Search & Load** - Find and use curated datasets with a few lines of code
- **Understand** - Rich schemas describe what each field means
- **Cite** - Automatic citation generation for publications
- **Publish** - Share your datasets with the community
- **AI-Ready** - MCP server for Claude and other AI assistants

## Quick Start

```bash
pip install foundry-ml
```

Need optional integrations? Install extras only when you need them:

```bash
pip install "foundry-ml[torch]"        # Enable dataset.get_as_torch()
pip install "foundry-ml[tensorflow]"   # Enable dataset.get_as_tensorflow()
pip install "foundry-ml[huggingface]"  # Enable push-to-hub
pip install "foundry-ml[excel]"        # Excel import support via openpyxl
```

> PyTorch/TensorFlow extras expect wheels compiled against NumPy 2.0. Install PyTorch 2.3+ and TensorFlow 2.18+ (or newer builds with NumPy 2 support) to avoid ABI errors.

```python
from foundry import Foundry

# Connect
f = Foundry()

# Search
results = f.search("band gap", limit=5)

# Load
dataset = results.iloc[0].FoundryDataset
X, y = dataset.get_as_dict()['train']

# Understand
schema = dataset.get_schema()
print(schema['fields'])

# Cite
print(dataset.get_citation())
```

## Cloud Environments

For Google Colab or remote Jupyter:

```python
f = Foundry(no_browser=True, no_local_server=True)
```

## CLI

```bash
foundry search "band gap"
foundry schema 10.18126/abc123
foundry --help
```

## AI Agent Integration

```bash
foundry mcp install  # Add to Claude Code
```

## Documentation

- [Getting Started](https://ai-materials-and-chemistry.gitbook.io/foundry/quickstart)
- [User Guide](https://ai-materials-and-chemistry.gitbook.io/foundry/)
- [API Reference](https://ai-materials-and-chemistry.gitbook.io/foundry/api/foundry)
- [Examples](./examples)

## Features

| Feature | Description |
|---------|-------------|
| Search | Find datasets by keyword, DOI, or browse catalog |
| Load | Automatic download, caching, and format conversion |
| PyTorch/TensorFlow (extras) | `dataset.get_as_torch()`, `dataset.get_as_tensorflow()` |
| CLI | Terminal-based workflows |
| MCP Server | AI assistant integration |
| HuggingFace Export (extra) | Publish to HuggingFace Hub |

## Available Datasets

Browse datasets at [Foundry-ML.org](https://foundry-ml.org/) or:

```python
f = Foundry()
f.list(limit=20)  # See available datasets
```

## How to Cite

If you use Foundry-ML, please cite:

```bibtex
@article{Schmidt2024,
  doi = {10.21105/joss.05467},
  year = {2024},
  publisher = {The Open Journal},
  volume = {9},
  number = {93},
  pages = {5467},
  author = {Kj Schmidt and Aristana Scourtas and Logan Ward and others},
  title = {Foundry-ML - Software and Services to Simplify Access to Machine Learning Datasets in Materials Science},
  journal = {Journal of Open Source Software}
}
```

## Contributing

Foundry is open source. To contribute:

1. Fork from `main`
2. Make your changes
3. Open a Pull Request

See [CONTRIBUTING.md](docs/how-to-contribute/contributing.md) for details.

## Support

This work was supported by the National Science Foundation under NSF Award Number: 1931306 "Collaborative Research: Framework: Machine Learning Materials Innovation Infrastructure".

Foundry integrates with [Materials Data Facility](https://materialsdatafacility.org), [FuncX](https://www.funcx.org), and [MAST-ML](https://mastmldocs.readthedocs.io/).
