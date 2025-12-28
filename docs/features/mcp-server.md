# MCP Server (AI Agent Integration)

Foundry includes an MCP (Model Context Protocol) server that enables AI assistants like Claude to discover and use materials science datasets.

## What is MCP?

MCP is a protocol that allows AI assistants to use external tools. With Foundry's MCP server, you can ask Claude:

- "Find me a materials science dataset for band gap prediction"
- "What fields are in the OQMD dataset?"
- "Load the training data and show me the first few rows"

## Quick Start

### Install for Claude Code

```bash
foundry mcp install
```

This adds Foundry to your Claude Code configuration. Restart Claude Code to activate.

### Manual Start

For custom integrations:

```bash
foundry mcp start
```

## Available Tools

The MCP server provides these tools to AI agents:

### search_datasets

Search for materials science datasets.

**Parameters:**
- `query` (string, required) - Search terms
- `limit` (integer, optional) - Maximum results (default: 10)

**Returns:** List of datasets with name, title, DOI, description

**Example prompt:** "Search for datasets about crystal structures"

### get_dataset_schema

Get the schema of a dataset - what fields it contains.

**Parameters:**
- `doi` (string, required) - The dataset DOI

**Returns:** Schema with splits, fields, data types, and descriptions

**Example prompt:** "What fields are in dataset 10.18126/abc123?"

### load_dataset

Load a dataset and return its data with schema.

**Parameters:**
- `doi` (string, required) - The dataset DOI
- `split` (string, optional) - Which split to load (default: all)

**Returns:** Data with schema information and citation

**Example prompt:** "Load the training data from the band gap dataset"

### list_all_datasets

List all available Foundry datasets.

**Parameters:**
- `limit` (integer, optional) - Maximum results (default: 100)

**Returns:** Complete catalog of available datasets

**Example prompt:** "What datasets are available in Foundry?"

## Configuration

### Claude Code

The `foundry mcp install` command adds this to your Claude Code config:

```json
{
  "mcpServers": {
    "foundry-ml": {
      "command": "foundry",
      "args": ["mcp", "start"]
    }
  }
}
```

### Custom Integration

For other MCP-compatible clients, the server uses stdio transport:

```python
from foundry.mcp.server import create_server

config = create_server()
# config contains server name, version, and tool definitions
```

## Example Conversations

### Finding a Dataset

**You:** Find me a dataset for predicting band gaps of materials

**Claude:** I'll search for band gap datasets in Foundry.

*Uses search_datasets tool*

I found 5 datasets related to band gaps:
1. **OQMD Band Gaps** (10.18126/abc) - 50,000 materials
2. **AFLOW Band Gaps** (10.18126/def) - 30,000 materials
...

### Understanding a Dataset

**You:** What's in the OQMD band gaps dataset?

**Claude:** Let me get the schema for that dataset.

*Uses get_dataset_schema tool*

The OQMD Band Gaps dataset contains:
- **Inputs:** composition (chemical formula), structure (crystal structure)
- **Targets:** band_gap (eV)
- **Splits:** train (80%), test (20%)

### Loading Data

**You:** Load the training data and show me some examples

**Claude:** I'll load the training split.

*Uses load_dataset tool*

Here are the first 5 rows:
| composition | band_gap |
|-------------|----------|
| Si | 1.12 |
| GaAs | 1.42 |
...

## Troubleshooting

### Server Not Starting

Ensure Foundry is installed correctly:

```bash
pip install --upgrade foundry-ml
foundry version
```

### Tools Not Available

Restart Claude Code after installing:

```bash
foundry mcp install
# Restart Claude Code
```

### Authentication Issues

For datasets requiring authentication, ensure you've authenticated:

```python
from foundry import Foundry
f = Foundry()  # This triggers auth flow if needed
```

## Technical Details

### Protocol

The MCP server uses JSON-RPC 2.0 over stdio.

### Server Info

```python
from foundry.mcp.server import create_server

config = create_server()
print(config)
# {
#   "name": "foundry-ml",
#   "version": "1.1.0",
#   "tools": [...]
# }
```

### Tool Definitions

Each tool follows the MCP tool schema:

```python
{
    "name": "search_datasets",
    "description": "Search for materials science datasets...",
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "..."},
            "limit": {"type": "integer", "default": 10}
        },
        "required": ["query"]
    }
}
```
