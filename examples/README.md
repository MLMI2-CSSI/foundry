# Examples using Foundry

If you're wondering how to get started with Foundry or want to see it in action, you're in the right place!

## Tutorials (Start Here)

| # | Name | Time | Description |
|---|------|------|-------------|
| 00 | [Hello Foundry](./00_hello_foundry/) | 5 min | Absolute basics - your first dataset |
| 01 | [Quickstart](./01_quickstart/) | 5 min | Search, load, use in ML workflow |
| 02 | [Working with Data](./02_working_with_data/) | 15 min | Schemas, splits, PyTorch/TensorFlow |
| 03 | [Advanced Workflows](./03_advanced_workflows/) | 20 min | Publishing, HuggingFace, CLI, MCP |

## Domain Examples

Each folder contains a notebook and `requirements.txt` file. The notebooks can be run locally or in [Google Colab](https://colab.research.google.com/).

| Example | Domain | Description |
|---------|--------|-------------|
| [bandgap](./bandgap/) | Materials | Band gap prediction |
| [oqmd](./oqmd/) | Materials | Open Quantum Materials Database |
| [zeolite](./zeolite/) | Chemistry | Zeolite structure analysis |
| [dendrite-segmentation](./dendrite-segmentation/) | Imaging | Microscopy segmentation |
| [atom-position-finding](./atom-position-finding/) | Imaging | Atom localization |

## Quick Reference

```python
from foundry import Foundry

f = Foundry()  # HTTPS download by default
results = f.search("band gap", limit=5)
dataset = results.iloc[0].FoundryDataset
X, y = dataset.get_as_dict()['train']
```

**Cloud environments (Colab, etc.):**
```python
f = Foundry(no_browser=True, no_local_server=True)
```

**For large datasets with Globus:**
```python
f = Foundry(use_globus=True)  # Requires Globus Connect Personal
```

**CLI:**
```bash
foundry search "band gap"
foundry schema <doi>
```

If you have any trouble, check our [documentation](https://ai-materials-and-chemistry.gitbook.io/foundry/v/docs/) or create an issue.
