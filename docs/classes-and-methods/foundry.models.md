# foundry.models

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L0)

## module `foundry.models`

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L19)

### class `FoundrySpecificationDataset`

Pydantic base class for datasets within the Foundry data package specification

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L27)

### class `FoundrySpecification`

Pydantic base class for interacting with the Foundry data package specification The specification provides a way to group datasets and manage versions

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L38)

#### method `add_dependency`

```python
add_dependency(name, version)
```

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L50)

#### method `clear_dependencies`

```python
clear_dependencies()
```

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L41)

#### method `remove_duplicate_dependencies`

```python
remove_duplicate_dependencies()
```

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L62)

### class `FoundryDatasetType`

Foundry Dataset Types Enumeration of the possible Foundry dataset types

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L73)

### class `FoundryKeyClass`

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L78)

### class `FoundryKey`

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L87)

### class `FoundrySplit`

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L93)

### class `FoundrySchema`

Foundry Dataset Schema for Foundry Datasets. This includes specifications of inputs, outputs, type, version, and more

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L131)

### class `FoundryDataset`

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L152)

### class `FoundryBase`

Configuration information for Foundry instance

**Args:**

* `dataframe_file` (str): Filename to read dataframe contents from
* `metadata_file` (str): Filename to read metadata contents from defaults to reading for MDF Discover
* `destination_endpoint` (str): Globus endpoint ID to transfer data to (defaults to local GCP installation)
* `local_cache_dir` (str): Path to local Foundry package cache

***

_This file was automatically generated via_ [_lazydocs_](https://github.com/ml-tooling/lazydocs)_._
