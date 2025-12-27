# Command Line Interface

Foundry includes a CLI for terminal-based workflows.

## Basic Usage

```bash
foundry --help
```

## Commands

### Search Datasets

```bash
# Search by keyword
foundry search "band gap"

# Limit results
foundry search "band gap" --limit 10

# JSON output (for scripting)
foundry search "band gap" --json
```

### Get Dataset Info

```bash
# Get info by DOI
foundry get 10.18126/abc123

# JSON output
foundry get 10.18126/abc123 --json
```

### View Schema

See what fields a dataset contains:

```bash
foundry schema 10.18126/abc123
```

Output:
```
Dataset: foundry_oqmd_band_gaps_v1.1
Data Type: tabular

Fields:
  - composition (input): Chemical composition
  - band_gap (target): Band gap value (eV)

Splits:
  - train
  - test
```

### List All Datasets

```bash
# List available datasets
foundry catalog

# Limit results
foundry catalog --limit 20

# JSON output
foundry catalog --json
```

### Check Publication Status

```bash
foundry status my_dataset_v1
```

### Version

```bash
foundry version
```

## HuggingFace Export

Export a Foundry dataset to HuggingFace Hub:

```bash
foundry push-to-hf 10.18126/abc123 --repo your-username/dataset-name
```

Options:
- `--repo` - HuggingFace repository ID (required)
- `--token` - HuggingFace API token (or set HF_TOKEN env var)
- `--private` - Create a private repository

## MCP Server

Start the MCP server for AI agent integration:

```bash
# Start server
foundry mcp start

# Install to Claude Code
foundry mcp install
```

See [MCP Server](mcp-server.md) for details.

## JSON Output

Most commands support `--json` for machine-readable output:

```bash
# Pipe to jq for processing
foundry catalog --json | jq '.[].name'

# Save to file
foundry search "crystal" --json > results.json
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (see message) |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `HF_TOKEN` | HuggingFace API token |
| `GLOBUS_TOKEN` | Globus authentication |

## Examples

### Find and Download a Dataset

```bash
# Search
foundry search "formation energy" --limit 5

# Get the DOI from results, then get details
foundry schema 10.18126/xyz789

# Use in Python
python -c "
from foundry import Foundry
f = Foundry()
ds = f.get_dataset('10.18126/xyz789')
print(ds.get_as_dict().keys())
"
```

### Export to HuggingFace

```bash
# Set token
export HF_TOKEN=hf_xxxxx

# Export
foundry push-to-hf 10.18126/abc123 --repo materials-science/my-dataset
```

### Scripting with JSON

```bash
#!/bin/bash
# Find all datasets with "band" in the name
foundry search "band" --json | jq -r '.[].doi' | while read doi; do
    echo "Processing: $doi"
    foundry schema "$doi"
done
```
