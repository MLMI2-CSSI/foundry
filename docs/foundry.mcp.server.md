<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mcp/server.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.mcp.server`
Foundry MCP Server Implementation. 

This server implements the Model Context Protocol (MCP) to allow AI agents to discover and interact with materials science datasets. 

Tools provided: 
- search_datasets: Search for datasets by query 
- get_dataset_schema: Get the schema of a specific dataset 
- load_dataset: Load data from a dataset 
- list_all_datasets: List all available datasets 

**Global Variables**
---------------
- **TOOLS**

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mcp/server.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `search_datasets`

```python
search_datasets(query: str, limit: int = 10) → List[Dict[str, Any]]
```

Search for materials science datasets. 



**Args:**
 
 - <b>`query`</b>:  Search terms (e.g., "band gap", "crystal structure", "zeolite") 
 - <b>`limit`</b>:  Maximum number of results to return (default: 10) 



**Returns:**
 List of datasets with name, title, DOI, and description 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mcp/server.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_dataset_schema`

```python
get_dataset_schema(doi: str) → Dict[str, Any]
```

Get the schema of a dataset - what fields it contains. 

Use this to understand the structure of a dataset before loading it. 



**Args:**
 
 - <b>`doi`</b>:  The DOI of the dataset (e.g., "10.18126/abc123") 



**Returns:**
 Schema with name, splits, fields (with descriptions and units), and data type 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mcp/server.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load_dataset`

```python
load_dataset(doi: str, split: str = 'train') → Dict[str, Any]
```

Load a dataset and return its data with schema. 

This downloads the data if not cached, then returns it along with schema information. 



**Args:**
 
 - <b>`doi`</b>:  The DOI of the dataset 
 - <b>`split`</b>:  Which split to load (default: "train") 



**Returns:**
 Dictionary with "schema" (field information) and "data" (the actual data) 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mcp/server.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `list_all_datasets`

```python
list_all_datasets(limit: int = 100) → List[Dict[str, Any]]
```

List all available Foundry datasets. 

Returns a catalog of all datasets that can be loaded. 



**Args:**
 
 - <b>`limit`</b>:  Maximum number of datasets to return (default: 100) 



**Returns:**
 List of all available datasets with basic info 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mcp/server.py#L231"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `handle_tool_call`

```python
handle_tool_call(name: str, arguments: Dict[str, Any]) → Any
```

Handle a tool call and return the result. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mcp/server.py#L251"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_server`

```python
create_server()
```

Create and return the MCP server configuration. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mcp/server.py#L261"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `run_server`

```python
run_server(host: str = 'localhost', port: int = 8765)
```

Run the MCP server using stdio transport. 

This implements a simple JSON-RPC style protocol for MCP. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
