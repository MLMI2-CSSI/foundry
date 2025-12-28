# HuggingFace Integration

Export Foundry datasets to HuggingFace Hub to increase visibility and enable discovery by the broader ML community.

## Installation

```bash
pip install foundry-ml[huggingface]
```

## Quick Start

### Python API

```python
from foundry import Foundry
from foundry.integrations.huggingface import push_to_hub

# Get a dataset
f = Foundry()
dataset = f.search("band gap", limit=1).iloc[0].FoundryDataset

# Export to HuggingFace Hub
url = push_to_hub(
    dataset,
    repo_id="your-username/dataset-name",
    token="hf_xxxxx"  # Or set HF_TOKEN env var
)
print(f"Published at: {url}")
```

### CLI

```bash
# Set your HuggingFace token
export HF_TOKEN=hf_xxxxx

# Export a dataset
foundry push-to-hf 10.18126/abc123 --repo your-username/dataset-name
```

## What Gets Created

When you export a dataset, Foundry creates:

### 1. Data Files

The dataset is converted to HuggingFace's format (Parquet/Arrow) with all splits preserved:

```
dataset/
  train/
    data-00000.parquet
  test/
    data-00000.parquet
```

### 2. Dataset Card (README.md)

A comprehensive README is auto-generated from the Foundry metadata:

```markdown
---
license: cc-by-4.0
tags:
  - materials-science
  - foundry-ml
---

# Band Gap Dataset

Calculated band gaps for 50,000 materials...

## Fields
| Field | Role | Description | Units |
|-------|------|-------------|-------|
| composition | input | Chemical formula | - |
| band_gap | target | DFT band gap | eV |

## Citation
@article{...}

## Source
Original DOI: 10.18126/abc123
```

### 3. Metadata

HuggingFace-compatible metadata including:
- License information
- Task categories
- Tags for discoverability
- Size information

## API Reference

### push_to_hub

```python
def push_to_hub(
    dataset,           # FoundryDataset object
    repo_id: str,      # HF Hub repo (e.g., "org/name")
    token: str = None, # HF API token
    private: bool = False,
    split: str = None  # Specific split to export
) -> str:  # Returns URL
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset` | FoundryDataset | Yes | Dataset from Foundry |
| `repo_id` | str | Yes | HuggingFace repository ID |
| `token` | str | No | API token (uses cached if not provided) |
| `private` | bool | No | Create private repository |
| `split` | str | No | Export specific split only |

**Returns:** URL of the created dataset

## Author Attribution

**Important:** The authors listed on HuggingFace come from the original DataCite metadata, not the person pushing. This preserves proper scientific attribution.

```python
# The original creators from DataCite metadata
authors = dataset.dc.creators
# e.g., [{"creatorName": "Smith, John"}, {"creatorName": "Doe, Jane"}]
```

## Examples

### Export All Splits

```python
from foundry import Foundry
from foundry.integrations.huggingface import push_to_hub

f = Foundry()
ds = f.get_dataset("10.18126/abc123")

url = push_to_hub(ds, "materials-science/band-gaps")
```

### Export Single Split

```python
url = push_to_hub(
    ds,
    "materials-science/band-gaps-train",
    split="train"
)
```

### Private Repository

```python
url = push_to_hub(
    ds,
    "my-org/private-dataset",
    private=True
)
```

### Using Environment Variable

```bash
export HF_TOKEN=hf_xxxxx
```

```python
# Token is picked up automatically
url = push_to_hub(ds, "org/name")
```

## CLI Options

```bash
foundry push-to-hf <doi> --repo <repo_id> [options]

Options:
  --repo TEXT     HuggingFace repository ID (required)
  --token TEXT    HuggingFace API token
  --private       Create private repository
  --help          Show this message
```

## Best Practices

### Repository Naming

Use descriptive, lowercase names with hyphens:
- Good: `materials-science/oqmd-band-gaps`
- Bad: `my_dataset_v1`

### Organization

Consider creating an organization for your lab/group:
- `your-lab/dataset-1`
- `your-lab/dataset-2`

### Documentation

The auto-generated README is a starting point. Consider adding:
- More detailed description
- Example usage code
- Related papers
- Acknowledgments

## Troubleshooting

### Authentication Failed

```python
# Ensure you're logged in
from huggingface_hub import login
login()  # Interactive login

# Or set token explicitly
push_to_hub(ds, "org/name", token="hf_xxxxx")
```

### Repository Already Exists

HuggingFace won't overwrite existing repos by default. Either:
1. Use a different repo name
2. Delete the existing repo first
3. Use the HuggingFace web interface to update

### Large Datasets

For very large datasets (>10GB), the upload may take time. Consider:
- Exporting specific splits: `split="train"`
- Using a stable internet connection
- Running in a cloud environment
