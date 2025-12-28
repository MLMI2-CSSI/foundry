# Searching for Datasets

Foundry provides multiple ways to discover datasets.

## Keyword Search

Search by topic, material, or property:

```python
from foundry import Foundry

f = Foundry()

# Search by keyword
results = f.search("band gap")
results = f.search("crystal structure")
results = f.search("formation energy")
```

### Limit Results

```python
results = f.search("band gap", limit=5)
```

### JSON Output

For programmatic access:

```python
results = f.search("band gap", as_json=True)

for ds in results:
    print(f"{ds['name']}: {ds['title']}")
```

## Browse the Catalog

List all available datasets:

```python
# List datasets
catalog = f.list(limit=20)

# As JSON
catalog = f.list(as_json=True)
```

## Get by DOI

If you know the DOI:

```python
dataset = f.get_dataset("10.18126/abc123")
```

## Search Results

Search returns a DataFrame with columns:

| Column | Description |
|--------|-------------|
| `dataset_name` | Unique identifier |
| `title` | Human-readable title |
| `DOI` | Digital Object Identifier |
| `year` | Publication year |
| `FoundryDataset` | Dataset object for loading |

## Accessing Datasets

From search results:

```python
# By index
dataset = results.iloc[0].FoundryDataset

# By name
dataset = results.get_dataset_by_name("foundry_oqmd_band_gaps_v1.1")

# By DOI
dataset = results.get_dataset_by_doi("10.18126/abc123")
```

## CLI Search

```bash
# Search from terminal
foundry search "band gap"

# Limit results
foundry search "band gap" --limit 5

# JSON output
foundry search "band gap" --json
```

## Tips

### Broad vs. Specific

```python
# Broad (more results)
f.search("energy")

# Specific (fewer, more relevant)
f.search("formation energy DFT")
```

### Check What's Available

```python
# See all datasets first
all_ds = f.list(limit=100)
print(f"Total datasets: {len(all_ds)}")

# Then search
results = f.search("your topic")
```

### Inspect Before Loading

```python
# Check schema before downloading
dataset = results.iloc[0].FoundryDataset
schema = dataset.get_schema()

print(f"Fields: {[f['name'] for f in schema['fields']]}")
print(f"Splits: {[s['name'] for s in schema['splits']]}")
```
