<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.foundry_dataset`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryDataset`
Representation of an individual dataset. Provides access to metadata as well as functions to instantiate data into memory in different formats. 

Desired functions: 
    - Get as pandas 
    - Get as tensorflow dataset 
    - Get as pytorch dataset 
    - Get file list 
    - Set metadata 
    - Attach datafiles 
    - Validate against schema 
    - Get citation 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(source_id: str, datacite_entry: dict, foundry_schema: FoundrySchema)
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_if_not_downloaded`

```python
download_if_not_downloaded()
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_citation`

```python
get_citation() → str
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_data`

```python
load_data(source_id=None, globus=True, as_hdf5=False, splits=[])
```

Load in the data associated with the prescribed dataset 

Tabular Data Type: Data are arranged in a standard data frame stored in self.dataframe_file. The contents are read, and 

File Data Type: <<Add desc>> 

For more complicated data structures, users should subclass FoundryDataset and override the load_data function 



**Args:**
 
 - <b>`inputs`</b> (list):  List of strings for input columns 
 - <b>`targets`</b> (list):  List of strings for output columns 
 - <b>`source_id`</b> (string):  Relative path to the source file 
 - <b>`as_hdf5`</b> (bool):  If True and dataset is in hdf5 format, keep data in hdf5 format 
 - <b>`splits`</b> (list):  Labels of splits to be loaded 



**Returns:**
 
 - <b>`(dict)`</b>:  a labeled dictionary of tuples 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_tensorflow`

```python
to_tensorflow(split: str = None)
```

Convert Foundry Dataset to a Tensorflow Sequence 



**Arguments:**
 
 - <b>`split`</b> (string):  Split to create Tensorflow Sequence on. 
 - <b>`**Default`</b>: ** ``None`` 

Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_dataset.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_torch`

```python
to_torch(split: str = None)
```

Convert Foundry Dataset to a PyTorch Dataset 



**Arguments:**
 
 - <b>`split`</b> (string):  Split to create PyTorch Dataset on. 
 - <b>`**Default`</b>: ** ``None`` 

Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split 

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
