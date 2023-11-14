<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.models`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundrySpecificationDataset`
Pydantic base class for datasets within the Foundry data package specification 





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundrySpecification`
Pydantic base class for interacting with the Foundry data package specification The specification provides a way to group datasets and manage versions 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_dependency`

```python
add_dependency(name, version)
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_dependencies`

```python
clear_dependencies()
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `remove_duplicate_dependencies`

```python
remove_duplicate_dependencies()
```






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryDatasetType`
Foundry Dataset Types Enumeration of the possible Foundry dataset types 





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryKeyClass`








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryKey`








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundrySplit`








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundrySchema`
Foundry Dataset Schema for Foundry Datasets. This includes specifications of inputs, outputs, type, version, and more 





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L110"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryDataset`








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryBase`
Configuration information for Foundry instance 



**Args:**
 
 - <b>`dataframe_file`</b> (str):  Filename to read dataframe contents from 
 - <b>`metadata_file`</b> (str):  Filename to read metadata contents from defaults to reading for MDF Discover 
 - <b>`destination_endpoint`</b> (str):  Globus endpoint ID to transfer data to (defaults to local GCP installation) 
 - <b>`local_cache_dir`</b> (str):  Path to local Foundry package cache 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
