<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.foundry_cache`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryCache`
The FoundryCache manages the local storage of FoundryDataset objects 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    forge_client: MDFClient,
    transfer_client: Any,
    use_globus,
    interval,
    parallel_https,
    verbose,
    local_cache_dir: str = None
)
```

Initializes a FoundryCache object. 



**Args:**
 
 - <b>`forge_client`</b> (MDFClient):  The MDF client object. 
 - <b>`transfer_client`</b> (Any):  The transfer client object. 
 - <b>`use_globus`</b> (bool):  Flag indicating whether to use Globus for downloading. 
 - <b>`interval`</b> (int):  How often to wait before checking Globus transfer status. 
 - <b>`parallel_https`</b> (int):  Number of threads to use for downloading via HTTP. 
 - <b>`verbose`</b> (bool):  Flag indicating whether to produce more debug messages. 
 - <b>`local_cache_dir`</b> (str, optional):  The local cache directory. Defaults to None.  If not specified, defaults to either the environmental variable 'FOUNDRY_LOCAL_CACHE_DIR'  or './data/'. 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L442"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_cache`

```python
clear_cache(dataset_name: str = None)
```

Deletes all of the locally stored datasets 



**Arguments:**
 
 - <b>`dataset_name`</b> (str):  Optional name of a specific dataset. If omitted,  all datsets will be erased 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_to_cache`

```python
download_to_cache(dataset_name: str, splits: List[Split] = None)
```

Checks if the data is downloaded, and if not, downloads the data from source to local storage. 



**Args:**
 
 - <b>`dataset_name`</b> (str):  Name of the dataset (equivalent to source_id in MDF). 
 - <b>`splits`</b> (List[FoundrySplit], optional):  List of splits in the dataset. Defaults to None. 



**Returns:**
 
 - <b>`FoundryCache`</b>:  The FoundryCache object. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_via_globus`

```python
download_via_globus(dataset_name: str)
```

Downloads selected dataset over Globus. 



**Args:**
 
 - <b>`dataset_name`</b> (str):  Name of the dataset (equivalent to source_id in MDF). 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_via_http`

```python
download_via_http(dataset_name: str)
```

Downloads selected dataset from MDF over HTTP. 

**Args:**
 dataset_name (str): Name of the dataset (equivalent to source_id in MDF). 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L408"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_as_dict`

```python
load_as_dict(
    split: str,
    dataset_name: str,
    foundry_schema: FoundrySchema,
    as_hdf5: bool
)
```

Load the data associated with the specified dataset and return it as a labeled dictionary of tuples. 



**Args:**
 
 - <b>`split`</b> (str):  Split to load the data from. 
 - <b>`dataset_name`</b> (str):  Name of the dataset (equivalent to source_id in MDF). 
 - <b>`foundry_schema`</b> (FoundrySchema, optional):  FoundrySchema object. Defaults to None. 
 - <b>`as_hdf5`</b> (bool, optional):  If True and dataset is in HDF5 format, keep data in HDF5 format. Defaults to False. 



**Returns:**
 
 - <b>`dict`</b>:  A labeled dictionary of tuples containing the loaded data. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L255"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_as_tensorflow`

```python
load_as_tensorflow(
    split: str,
    dataset_name: str,
    foundry_schema: FoundrySchema,
    as_hdf5: bool
)
```

Convert Foundry Dataset to a Tensorflow Sequence 



**Arguments:**
 
 - <b>`split`</b> (string):  Split to create Tensorflow Sequence on. 
 - <b>`**Default`</b>: ** ``None`` 

Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L227"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_as_torch`

```python
load_as_torch(
    split: str,
    dataset_name: str,
    foundry_schema: FoundrySchema,
    as_hdf5: bool
)
```

Convert Foundry Dataset to a PyTorch Dataset 



**Arguments:**
 
 - <b>`split`</b> (string):  Split to create PyTorch Dataset on. 
 - <b>`**Default`</b>: ** ``None`` 

Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L130"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `validate_local_dataset_storage`

```python
validate_local_dataset_storage(dataset_name: str, splits: List[Split] = None)
```

Verifies that the local storage location exists and all expected files are present. 



**Args:**
 
 - <b>`dataset_name`</b> (str):  Name of the dataset (equivalent to source_id in MDF). 
 - <b>`splits`</b> (List[FoundrySplit], optional):  Labels of splits to be loaded. Defaults to None. 



**Returns:**
 
 - <b>`bool`</b>:  True if the dataset exists and contains all the desired files; False otherwise. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
