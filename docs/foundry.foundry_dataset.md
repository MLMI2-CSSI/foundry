<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.foundry_dataset`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryDataset`
Representation of an individual dataset. Provides access to metadata as well as functions to instantiate data into memory in different formats. 



**Args:**
 
 - <b>`dataset_name`</b> (str):  Name of the dataset (equivalent to source_id in MDF) 
 - <b>`datacite_entry`</b> (FoundryDatacite):  Datacite entry for the dataset 
 - <b>`foundry_schema`</b> (FoundrySchema):  Schema for the dataset 
 - <b>`foundry_cache`</b> (FoundryCache):  Cache for the dataset 

Desired functions: 
    - Get as pandas 
    - Get as tensorflow dataset 
    - Get as pytorch dataset 
    - Get file list 
    - Set metadata 
    - Attach datafiles 
    - Validate against schema 
    - Get citation 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    dataset_name: str,
    datacite_entry: FoundryDatacite,
    foundry_schema: FoundrySchema,
    foundry_cache: FoundryCache = None
)
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_data`

```python
add_data(local_data_path: str = None, globus_data_source: str = None)
```

Add data to the dataset. User must provide the location of the data as either a `globus_data_source` or `local_data_path`. 



**Arguments:**
 
 - <b>`local_data_path`</b> (str):  Local path to the dataset used to publish to Foundry via HTTPS. Creates an HTTPS PUT request to upload the data specified to a Globus endpoint (default is NCSA endpoint) before it is transferred to MDF. If None, the user must specify a 'globus_data_source' URL to the location of the data on their own Globus endpoint. User must choose either `globus_data_source` or `local_data_path` to publish their data. 
 - <b>`globus_data_source`</b> (str):  Url path for a data folder on a Globus endpoint; url can be obtained through  the Globus Web UI or SDK. If None, the user must specify an 'local_data_path' pointing to the location  of the data on their local machine. User must choose either `globus_data_source` or `local_data_path` to  publish their data. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L169"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clean_dc_dict`

```python
clean_dc_dict()
```

Clean the Datacite dictionary of None values 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_dataset_cache`

```python
clear_dataset_cache()
```

Deletes the cached data for this specific datset 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete_none`

```python
delete_none(_dict)
```

Delete None values recursively from all of the dictionaries 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_citation`

```python
get_citation() → str
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L110"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
