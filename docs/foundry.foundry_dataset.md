<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.foundry_dataset`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryDataset`
Representation of an individual dataset. Provides access to metadata as well as functions to instantiate data into memory in different formats. 



**Args:**
 
 - <b>`dataset_name`</b> (str):  name of dataset (equivalent to source_id in MDF) 
 - <b>`splits List[FoundrySplit]`</b>:  list of splits in the dataset 
 - <b>`use_globus`</b> (bool):  if True, use Globus to download the data else try HTTPS 
 - <b>`interval`</b> (int):  How often to wait before checking Globus transfer status 
 - <b>`parallel_https`</b> (int):  Number of files to download in parallel if using HTTPS 
 - <b>`verbose`</b> (bool):  Produce more debug messages to screen 

Desired functions: 
    - Get as pandas 
    - Get as tensorflow dataset 
    - Get as pytorch dataset 
    - Get file list 
    - Set metadata 
    - Attach datafiles 
    - Validate against schema 
    - Get citation 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    dataset_name: str,
    datacite_entry: dict,
    transfer_client: Any,
    foundry_schema: FoundrySchema,
    use_globus: bool = False,
    interval: int = 10,
    parallel_https: int = 4,
    verbose: bool = False,
    forge_client: Forge = None,
    local_cache_dir: str = None
)
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L160"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_dataset_cache`

```python
clear_dataset_cache()
```

Deletes the cached data for this specific datset 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_as_dict`

```python
get_as_dict(split: str = None, as_hdf5: bool = False)
```

Returns the data from the dataset as a dictionary 



**Arguments:**
 
 - <b>`split`</b> (string):  Split to create dataset on. 
 - <b>`**Default`</b>: ** ``None`` 

Returns: (dict) Dictionary of all the data from the specified split 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_as_tensorflow`

```python
get_as_tensorflow(split: str = None)
```

Convert Foundry Dataset to a Tensorflow Sequence 



**Arguments:**
 
 - <b>`split`</b> (string):  Split to create Tensorflow Sequence on. 
 - <b>`**Default`</b>: ** ``None`` 

Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_as_torch`

```python
get_as_torch(split: str = None)
```

Returns the data from the dataset as a TorchDataset 



**Arguments:**
 
 - <b>`split`</b> (string):  Split to create PyTorch Dataset on. 
 - <b>`**Default`</b>: ** ``None`` 

Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_citation`

```python
get_citation() → str
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L136"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `validate_metadata`

```python
validate_metadata(metadata)
```

Validate the JSON message against the FoundryDataset model 



**Arguments:**
 
 - <b>`metadata`</b> (dict):  Metadata information provided by the user. 



**Raises:**
 
 - <b>`ValidationError`</b>:  if metadata supplied by user does not meet the specificiation of a FoundryDataset object. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
