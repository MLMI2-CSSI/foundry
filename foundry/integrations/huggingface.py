"""Hugging Face Hub integration for Foundry datasets.

This module provides functionality to export Foundry datasets to Hugging Face Hub,
making materials science datasets discoverable in the broader ML ecosystem.

Requirements:
    pip install foundry-ml[huggingface]

Usage:
    from foundry import Foundry
    from foundry.integrations.huggingface import push_to_hub

    f = Foundry()
    dataset = f.get_dataset("10.18126/abc123")
    push_to_hub(dataset, "materials-science/bandgap-data")
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

try:
    from datasets import Dataset, DatasetDict
    from huggingface_hub import HfApi
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False


def _check_hf_available():
    """Check if HuggingFace dependencies are installed."""
    if not HF_AVAILABLE:
        raise ImportError(
            "HuggingFace integration requires additional dependencies. "
            "Install with: pip install foundry-ml[huggingface]"
        )


def push_to_hub(
    dataset,  # FoundryDataset
    repo_id: str,
    token: Optional[str] = None,
    private: bool = False,
    split: Optional[str] = None,
) -> str:
    """Export a Foundry dataset to Hugging Face Hub.

    This creates a new dataset repository on HF Hub with the Foundry data,
    automatically generating a Dataset Card from the DataCite metadata.

    Args:
        dataset: A FoundryDataset object (from foundry.get_dataset())
        repo_id: HF Hub repository ID (e.g., "materials-science/bandgap-data")
        token: HuggingFace API token. If None, uses cached credentials.
        private: If True, create a private repository.
        split: Specific split to export. If None, exports all splits.

    Returns:
        str: URL of the created dataset on HF Hub.

    Example:
        >>> from foundry import Foundry
        >>> from foundry.integrations.huggingface import push_to_hub
        >>> f = Foundry()
        >>> ds = f.get_dataset("10.18126/abc123")
        >>> url = push_to_hub(ds, "my-org/my-dataset")
        >>> print(f"Dataset published at: {url}")
    """
    _check_hf_available()

    logger.info(f"Exporting Foundry dataset '{dataset.dataset_name}' to HF Hub: {repo_id}")

    # Load data from Foundry
    data = dataset.get_as_dict(split=split)

    # Convert to HuggingFace Dataset format
    if isinstance(data, dict) and all(isinstance(v, tuple) for v in data.values()):
        # Data has splits: {split_name: (inputs, targets)}
        hf_datasets = {}
        for split_name, (inputs, targets) in data.items():
            combined = _combine_inputs_targets(inputs, targets)
            hf_datasets[split_name] = Dataset.from_dict(combined)
        hf_dataset = DatasetDict(hf_datasets)
    else:
        # Single dataset without splits
        hf_dataset = Dataset.from_dict(_flatten_data(data))

    # Generate Dataset Card (README.md) from DataCite metadata
    readme_content = _generate_dataset_card(dataset)

    # Push to Hub
    hf_dataset.push_to_hub(
        repo_id,
        token=token,
        private=private,
    )

    # Update the README with our generated card
    api = HfApi(token=token)
    api.upload_file(
        path_or_fileobj=readme_content.encode(),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="dataset",
    )

    url = f"https://huggingface.co/datasets/{repo_id}"
    logger.info(f"Successfully published to: {url}")
    return url


def _combine_inputs_targets(inputs: Dict, targets: Dict) -> Dict[str, Any]:
    """Combine input and target dictionaries into a single flat dict."""
    combined = {}

    for key, value in inputs.items():
        col_name = f"input_{key}" if key in targets else key
        combined[col_name] = _to_list(value)

    for key, value in targets.items():
        col_name = f"target_{key}" if key in inputs else key
        combined[col_name] = _to_list(value)

    return combined


def _flatten_data(data: Any) -> Dict[str, Any]:
    """Flatten nested data structure to a dict suitable for HF Dataset."""
    import pandas as pd

    if isinstance(data, pd.DataFrame):
        return {col: data[col].tolist() for col in data.columns}
    elif isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = _to_list(value)
        return result
    else:
        return {"data": _to_list(data)}


def _to_list(value: Any) -> list:
    """Convert various types to list for HF compatibility."""
    import pandas as pd
    import numpy as np

    if isinstance(value, np.ndarray):
        return value.tolist()
    elif isinstance(value, pd.Series):
        return value.tolist()
    elif isinstance(value, pd.DataFrame):
        return value.to_dict(orient='records')
    elif isinstance(value, (list, tuple)):
        return list(value)
    else:
        return [value]


def _normalize_license(license_str: str) -> str:
    """Map license string to a valid HuggingFace license identifier."""
    if not license_str:
        return "other"

    license_lower = license_str.lower()

    # Direct matches to HF identifiers
    hf_licenses = {
        "cc0", "cc0-1.0", "cc-by-4.0", "cc-by-sa-4.0", "cc-by-nc-4.0",
        "cc-by-nc-sa-4.0", "cc-by-nc-nd-4.0", "mit", "apache-2.0",
        "bsd", "bsd-2-clause", "bsd-3-clause", "gpl-3.0", "lgpl-3.0",
        "unknown", "other"
    }

    # Check for direct match
    if license_lower in hf_licenses:
        return license_lower

    # Common mappings
    mappings = {
        "creative commons": "cc-by-4.0",
        "cc by": "cc-by-4.0",
        "cc-by": "cc-by-4.0",
        "cc by 4": "cc-by-4.0",
        "cc by-sa": "cc-by-sa-4.0",
        "cc by-nc": "cc-by-nc-4.0",
        "cc0": "cc0-1.0",
        "public domain": "cc0-1.0",
        "apache": "apache-2.0",
        "mit license": "mit",
        "bsd license": "bsd-3-clause",
        "gpl": "gpl-3.0",
        "lgpl": "lgpl-3.0",
    }

    for pattern, hf_id in mappings.items():
        if pattern in license_lower:
            return hf_id

    # If we can't map it, use "other"
    return "other"


def _generate_dataset_card(dataset) -> str:
    """Generate a HuggingFace Dataset Card from Foundry DataCite metadata."""
    dc = dataset.dc
    schema = dataset.foundry_schema

    # Extract metadata
    title = dc.titles[0].title if dc.titles else dataset.dataset_name
    description = dc.descriptions[0].description if dc.descriptions else ""

    # DOI is a RootModel with .root containing the actual string
    doi = ""
    if dc.identifier and dc.identifier.identifier:
        doi_obj = dc.identifier.identifier
        doi = doi_obj.root if hasattr(doi_obj, 'root') else str(doi_obj)

    # Handle creators (can be dicts or pydantic objects)
    authors = []
    for c in (dc.creators or []):
        if isinstance(c, dict):
            authors.append(c.get('creatorName', 'Unknown'))
        elif hasattr(c, 'creatorName'):
            authors.append(c.creatorName or 'Unknown')
        else:
            authors.append(str(c))

    # Year is a RootModel with .root containing the actual int
    year = ""
    if hasattr(dc, 'publicationYear') and dc.publicationYear:
        year_obj = dc.publicationYear
        year = year_obj.root if hasattr(year_obj, 'root') else str(year_obj)

    # Get license if available (rightsList contains RightsListItem objects)
    license_raw = None
    if hasattr(dc, 'rightsList') and dc.rightsList:
        rights_item = dc.rightsList[0]
        if isinstance(rights_item, dict):
            license_raw = rights_item.get('rights')
        elif hasattr(rights_item, 'rights'):
            license_raw = rights_item.rights

    license_id = _normalize_license(license_raw)
    # For display, show original if different from ID
    license_display = license_raw if license_raw and license_raw != license_id else license_id

    # Build field documentation
    fields_doc = ""
    if schema.keys:
        fields_doc = "\n### Fields\n\n| Field | Role | Description | Units |\n|-------|------|-------------|-------|\n"
        for key in schema.keys:
            name = key.key[0] if key.key else "N/A"
            role = key.type or "N/A"
            desc = (key.description or "")[:50]
            units = key.units or ""
            fields_doc += f"| {name} | {role} | {desc} | {units} |\n"

    # Build splits documentation
    splits_doc = ""
    if schema.splits:
        splits_doc = "\n### Splits\n\n"
        for split in schema.splits:
            splits_doc += f"- **{split.label}**: {split.type or 'data'}\n"

    # Generate citation
    citation = dataset.get_citation()

    return f"""---
license: {license_id}
task_categories:
  - tabular-regression
  - tabular-classification
tags:
  - materials-science
  - chemistry
  - foundry-ml
  - scientific-data
size_categories:
  - 1K<n<10K
---

# {title}

{description}

## Dataset Information

- **Source**: [Foundry-ML](https://github.com/MLMI2-CSSI/foundry)
- **DOI**: [{doi}](https://doi.org/{doi})
- **Year**: {year}
- **Authors**: {', '.join(authors)}
- **Data Type**: {schema.data_type or 'tabular'}
{fields_doc}
{splits_doc}

## Usage

### With Foundry-ML (recommended for materials science workflows)

```python
from foundry import Foundry

f = Foundry()
dataset = f.get_dataset("{doi}")
X, y = dataset.get_as_dict()['train']
```

### With HuggingFace Datasets

```python
from datasets import load_dataset

dataset = load_dataset("{dataset.dataset_name}")
```

## Citation

```bibtex
{citation}
```

## License

{license_display}

---

*This dataset was exported from [Foundry-ML](https://github.com/MLMI2-CSSI/foundry), a platform for materials science datasets.*
"""
