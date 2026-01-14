"""Foundry MCP Server Implementation.

This server implements the Model Context Protocol (MCP) to allow AI agents
to discover and interact with materials science datasets.

Tools provided:
- search_datasets: Search for datasets by query
- get_dataset_schema: Get the schema of a specific dataset
- load_dataset: Load data from a dataset
- list_all_datasets: List all available datasets
"""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def _get_foundry():
    """Get a Foundry client instance for headless operation."""
    from foundry import Foundry
    return Foundry(no_browser=True, no_local_server=True)


def search_datasets(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search for materials science datasets.

    Args:
        query: Search terms (e.g., "band gap", "crystal structure", "zeolite")
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of datasets with name, title, DOI, and description
    """
    f = _get_foundry()
    results = f.search(query, limit=limit)

    output = []
    for _, row in results.iterrows():
        ds = row.FoundryDataset
        output.append({
            "name": ds.dataset_name,
            "title": ds.dc.titles[0].title if ds.dc.titles else None,
            "doi": str(ds.dc.identifier.identifier) if ds.dc.identifier else None,
            "description": ds.dc.descriptions[0].description if ds.dc.descriptions else None,
            "year": ds.dc.publicationYear if hasattr(ds.dc, 'publicationYear') else None,
        })
    return output


def get_dataset_schema(doi: str) -> Dict[str, Any]:
    """Get the schema of a dataset - what fields it contains.

    Use this to understand the structure of a dataset before loading it.

    Args:
        doi: The DOI of the dataset (e.g., "10.18126/abc123")

    Returns:
        Schema with name, splits, fields (with descriptions and units), and data type
    """
    f = _get_foundry()
    ds = f.get_dataset(doi)

    return {
        "name": ds.dataset_name,
        "title": ds.dc.titles[0].title if ds.dc.titles else None,
        "doi": str(ds.dc.identifier.identifier) if ds.dc.identifier else None,
        "data_type": ds.foundry_schema.data_type,
        "splits": [
            {"name": s.label, "type": s.type}
            for s in (ds.foundry_schema.splits or [])
        ],
        "fields": [
            {
                "name": k.key[0] if k.key else None,
                "role": k.type,  # "input" or "target"
                "description": k.description,
                "units": k.units,
            }
            for k in (ds.foundry_schema.keys or [])
        ],
    }


def load_dataset(doi: str, split: str = "train") -> Dict[str, Any]:
    """Load a dataset and return its data with schema.

    This downloads the data if not cached, then returns it along with schema information.

    Args:
        doi: The DOI of the dataset
        split: Which split to load (default: "train")

    Returns:
        Dictionary with "schema" (field information) and "data" (the actual data)
    """
    f = _get_foundry()
    ds = f.get_dataset(doi)
    data = ds.get_as_dict(split=split)
    schema = get_dataset_schema(doi)

    return {
        "schema": schema,
        "data": _serialize_data(data),
        "citation": ds.get_citation(),
    }


def list_all_datasets(limit: int = 100) -> List[Dict[str, Any]]:
    """List all available Foundry datasets.

    Returns a catalog of all datasets that can be loaded.

    Args:
        limit: Maximum number of datasets to return (default: 100)

    Returns:
        List of all available datasets with basic info
    """
    f = _get_foundry()
    results = f.list(limit=limit)

    output = []
    for _, row in results.iterrows():
        ds = row.FoundryDataset
        output.append({
            "name": ds.dataset_name,
            "title": ds.dc.titles[0].title if ds.dc.titles else None,
            "doi": str(ds.dc.identifier.identifier) if ds.dc.identifier else None,
            "description": ds.dc.descriptions[0].description if ds.dc.descriptions else None,
        })
    return output


def _serialize_data(data: Any) -> Any:
    """Convert numpy arrays and other non-JSON-serializable types to lists."""
    import numpy as np
    import pandas as pd

    if isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, pd.DataFrame):
        return data.to_dict(orient='records')
    elif isinstance(data, pd.Series):
        return data.tolist()
    elif isinstance(data, dict):
        return {k: _serialize_data(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [_serialize_data(item) for item in data]
    elif isinstance(data, (np.integer, np.floating)):
        return data.item()
    else:
        return data


# MCP Server Implementation using stdio transport
TOOLS = [
    {
        "name": "search_datasets",
        "description": "Search for materials science datasets. Returns datasets matching the query with name, title, DOI, and description.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search terms (e.g., 'band gap', 'crystal structure', 'zeolite')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results (default: 10)",
                    "default": 10
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_dataset_schema",
        "description": "Get the schema of a dataset - what fields it contains, their descriptions, "
                       "and units. Use this to understand the data structure before loading.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "doi": {
                    "type": "string",
                    "description": "The DOI of the dataset (e.g., '10.18126/abc123')"
                }
            },
            "required": ["doi"]
        }
    },
    {
        "name": "load_dataset",
        "description": "Load a dataset and return its data with schema information. Downloads data if not cached.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "doi": {
                    "type": "string",
                    "description": "The DOI of the dataset"
                },
                "split": {
                    "type": "string",
                    "description": "Which split to load (default: 'train')",
                    "default": "train"
                }
            },
            "required": ["doi"]
        }
    },
    {
        "name": "list_all_datasets",
        "description": "List all available Foundry datasets. Returns a catalog with basic info for each dataset.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of datasets to return (default: 100)",
                    "default": 100
                }
            },
            "required": []
        }
    }
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Any:
    """Handle a tool call and return the result."""
    if name == "search_datasets":
        return search_datasets(
            query=arguments["query"],
            limit=arguments.get("limit", 10)
        )
    elif name == "get_dataset_schema":
        return get_dataset_schema(doi=arguments["doi"])
    elif name == "load_dataset":
        return load_dataset(
            doi=arguments["doi"],
            split=arguments.get("split", "train")
        )
    elif name == "list_all_datasets":
        return list_all_datasets(limit=arguments.get("limit", 100))
    else:
        raise ValueError(f"Unknown tool: {name}")


def create_server():
    """Create and return the MCP server configuration."""
    return {
        "name": "foundry-ml",
        "version": "1.0.0",
        "description": "Materials science dataset discovery and loading for ML",
        "tools": TOOLS,
    }


def run_server(host: str = "localhost", port: int = 8765):
    """Run the MCP server using stdio transport.

    This implements a simple JSON-RPC style protocol for MCP.
    """
    import sys

    logger.info(f"Starting Foundry MCP server on {host}:{port}")

    # For now, use a simple stdio-based protocol
    # In production, this would use the full MCP SDK
    print(json.dumps({
        "jsonrpc": "2.0",
        "method": "server/info",
        "params": create_server()
    }), flush=True)

    # Read and process requests
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            method = request.get("method", "")

            if method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                try:
                    result = handle_tool_call(tool_name, arguments)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {"content": [{"type": "text", "text": json.dumps(result, default=str)}]}
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {"code": -32000, "message": str(e)}
                    }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }

            print(json.dumps(response), flush=True)

        except json.JSONDecodeError:
            continue
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }), flush=True)
