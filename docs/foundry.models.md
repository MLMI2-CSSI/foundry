<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.models`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundrySpecificationDataset`
Pydantic base class for datasets within the Foundry data package specification 





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundrySpecification`
Pydantic base class for interacting with the Foundry data package specification The specification provides a way to group datasets and manage versions 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_dependency`

```python
add_dependency(name, version)
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_dependencies`

```python
clear_dependencies()
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `remove_duplicate_dependencies`

```python
remove_duplicate_dependencies()
```






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryDatasetType`
Foundry Dataset Types Enumeration of the possible Foundry dataset types 





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundrySchema`
A model for the Foundry schema based on the FoundryModel (project_model.py) class. The FoundryModel class is an auto-generated pydantic version of the json schema; this class extends the FoundryModel class to include additional functionality necessary for Foundry. 



**Args:**
 
 - <b>`project_dict`</b> (dict):  A dictionary containing the project data. 



**Raises:**
 
 - <b>`ValidationError`</b>:  If there is an issue validating the project data. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(project_dict)
```









---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryDatacite`
A model for the Datacite schema based on the Datacite (dc_model.py) class. The FoundryModel class is an auto-generated pydantic version of the json schema; this class extends the DataciteModel class to include additional functionality necessary for Foundry. 



**Args:**
 
 - <b>`datacite_dict`</b> (dict):  A dictionary containing the datacite data. 



**Raises:**
 
 - <b>`ValidationError`</b>:  If there is an issue validating the datacite data. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L110"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(datacite_dict, extra=<Extra.allow: 'allow'>)
```









---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L132"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryBase`
Configuration information for Foundry instance 



**Args:**
 
 - <b>`dataframe_file`</b> (str, optional):  Filename to read dataframe contents from (default is "foundry_dataframe.json") 
 - <b>`data_file`</b> (str, optional):  Filename to read data contents from (default is "foundry.hdf5") 
 - <b>`metadata_file`</b> (str, optional):  Filename to read metadata contents from (default is "foundry_metadata.json") 
 - <b>`destination_endpoint`</b> (str, optional):  Globus endpoint ID to transfer data to (default is None) 
 - <b>`local`</b> (bool, optional):  Flag indicating whether to use local cache (default is False) 
 - <b>`local_cache_dir`</b> (str, optional):  Path to local Foundry package cache (default is "./data") 
 - <b>`metadata_key`</b> (str, optional):  Key for metadata (default is "foundry") 
 - <b>`organization`</b> (str, optional):  Organization name (default is "foundry") 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
