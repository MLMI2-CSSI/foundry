<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.foundry_cache`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryCache`
The FoundryCache manages the local storage of FoundryDataset objects 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(forge_client: Forge, transfer_client: Any, local_cache_dir: str = None)
```

Initializes a FoundryCache object. 



**Args:**
 
 - <b>`forge_client`</b> (Forge):  The Forge client object. 
 - <b>`transfer_client`</b> (Any):  The transfer client object. 
 - <b>`local_cache_dir`</b> (str, optional):  The local cache directory. Defaults to None.  If not specified, defaults to either environmental variable  ('FOUNDRY_LOCAL_CACHE_DIR') or './data/'. 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L461"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_cache`

```python
clear_cache(dataset_name: str = None)
```

Deletes all of the locally stored datasets 



**Arguments:**
 
 - <b>`dataset_name`</b> (str):  Optional name of a specific dataset. If omitted,  all datsets will be erased 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_to_cache`

```python
download_to_cache(
    dataset_name: str,
    splits: List[FoundrySplit] = None,
    use_globus: bool = False,
    interval: int = 10,
    parallel_https: int = 4,
    verbose: bool = False,
    transfer_client=None
)
```

Checks if the data is downloaded, and if not, downloads the data from source to local storage. 



**Args:**
 
 - <b>`dataset_name`</b> (str):  Name of the dataset (equivalent to source_id in MDF). 
 - <b>`splits`</b> (List[FoundrySplit], optional):  List of splits in the dataset. Defaults to None. 
 - <b>`use_globus`</b> (bool, optional):  If True, use Globus to download the data; otherwise, try HTTPS. Defaults to False. 
 - <b>`interval`</b> (int, optional):  How often to wait before checking Globus transfer status. Defaults to 10. 
 - <b>`parallel_https`</b> (int, optional):  Number of files to download in parallel if using HTTPS. Defaults to 4. 
 - <b>`verbose`</b> (bool, optional):  Produce more debug messages to screen. Defaults to False. 
 - <b>`transfer_client`</b> (Any, optional):  The transfer client object. Defaults to None. 



**Returns:**
 
 - <b>`FoundryCache`</b>:  The FoundryCache object. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_via_globus`

```python
download_via_globus(dataset_name: str, interval: int)
```

Downloads selected dataset over Globus. 



**Args:**
 
 - <b>`dataset_name`</b> (str):  Name of the dataset (equivalent to source_id in MDF). 
 - <b>`interval`</b> (int):  How often to wait before checking Globus transfer status. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_via_http`

```python
download_via_http(
    dataset_name: str,
    parallel_https: int,
    verbose: bool,
    transfer_client: Any
)
```

Downloads selected dataset from MDF over HTTP. 



**Args:**
 
 - <b>`dataset_name`</b> (str):  Name of the dataset (equivalent to source_id in MDF). 
 - <b>`parallel_https`</b> (int):  Number of threads to use for downloading. 
 - <b>`verbose`</b> (bool):  Produce more debug messages to screen. 
 - <b>`transfer_client`</b> (Any):  The transfer client object. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L427"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_keys`

```python
get_keys(
    foundry_schema: FoundrySchema,
    type: str = None,
    as_object: bool = False
)
```

Get keys for a Foundry dataset 



**Arguments:**
 
 - <b>`foundry_schema`</b> (FoundrySchema):  The schema from MDF that contains the keys 
 - <b>`type`</b> (str):  The type of key to be returned e.g., "input", "target" 
 - <b>`as_object`</b> (bool):  When ``False``, will return a list of keys in as strings  When ``True``, will return the full key objects 
 - <b>`**Default`</b>: ** ``False`` Returns: (list) String representations of keys or if ``as_object`` is False otherwise returns the full key objects. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L181"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_as_dict`

```python
load_as_dict(
    split: str,
    dataset_name: str,
    foundry_schema: FoundrySchema,
    use_globus: bool,
    interval: int,
    parallel_https: int,
    verbose: bool,
    transfer_client: Any,
    as_hdf5: bool
)
```

Load in the data associated with the prescribed dataset. 



**Args:**
 
 - <b>`dataset_name`</b> (str):  Name of the dataset (equivalent to source_id in MDF). 
 - <b>`foundry_schema`</b> (FoundrySchema, optional):  Schema element as obtained from MDF. Defaults to None. 
 - <b>`use_globus`</b> (bool, optional):  If True, use Globus to download the data; otherwise, try HTTPS. Defaults to False. 
 - <b>`interval`</b> (int, optional):  How often to wait before checking Globus transfer status. Defaults to 10. 
 - <b>`parallel_https`</b> (int, optional):  Number of files to download in parallel if using HTTPS. Defaults to 4. 
 - <b>`verbose`</b> (bool, optional):  Produce more debug messages to screen. Defaults to False. 
 - <b>`transfer_client`</b> (Any, optional):  The transfer client object. Defaults to None. 
 - <b>`as_hdf5`</b> (bool, optional):  If True and dataset is in HDF5 format, keep data in HDF5 format. Defaults to False. 



**Returns:**
 
 - <b>`dict`</b>:  A labeled dictionary of tuples. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L270"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_as_tensorflow`

```python
load_as_tensorflow(
    split: str,
    dataset_name: str,
    foundry_schema: FoundrySchema,
    use_globus: bool,
    interval: int,
    parallel_https: int,
    verbose: bool,
    transfer_client: Any,
    as_hdf5: bool
)
```

Convert Foundry Dataset to a Tensorflow Sequence 



**Arguments:**
 
 - <b>`split`</b> (string):  Split to create Tensorflow Sequence on. 
 - <b>`**Default`</b>: ** ``None`` 

Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L237"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_as_torch`

```python
load_as_torch(
    split: str,
    dataset_name: str,
    foundry_schema: FoundrySchema,
    use_globus: bool,
    interval: int,
    parallel_https: int,
    verbose: bool,
    transfer_client: Any,
    as_hdf5: bool
)
```

Convert Foundry Dataset to a PyTorch Dataset 



**Arguments:**
 
 - <b>`split`</b> (string):  Split to create PyTorch Dataset on. 
 - <b>`**Default`</b>: ** ``None`` 

Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L138"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `validate_local_dataset_storage`

```python
validate_local_dataset_storage(
    dataset_name: str,
    splits: List[FoundrySplit] = None
)
```

Verifies that the local storage location exists and all expected files are present. 



**Args:**
 
 - <b>`dataset_name`</b> (str):  Name of the dataset (equivalent to source_id in MDF). 
 - <b>`splits`</b> (List[FoundrySplit], optional):  Labels of splits to be loaded. Defaults to None. 



**Returns:**
 
 - <b>`bool`</b>:  True if the dataset exists and contains all the desired files; False otherwise. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
