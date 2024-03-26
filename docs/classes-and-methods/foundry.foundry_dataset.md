# foundry.foundry\_dataset

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_dataset.py#L0)

## module `foundry.foundry_dataset`

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_dataset.py#L15)

### class `FoundryDataset`

Representation of an individual dataset. Provides access to metadata as well as functions to instantiate data into memory in different formats.

**Args:**

* `dataset_name` (str): name of dataset (equivalent to source\_id in MDF)
* `splits List[FoundrySplit]`: list of splits in the dataset
* `use_globus` (bool): if True, use Globus to download the data else try HTTPS
* `interval` (int): How often to wait before checking Globus transfer status
* `parallel_https` (int): Number of files to download in parallel if using HTTPS
* `verbose` (bool): Produce more debug messages to screen

Desired functions: - Get as pandas - Get as tensorflow dataset - Get as pytorch dataset - Get file list - Set metadata - Attach datafiles - Validate against schema - Get citation

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_dataset.py#L39)

#### method `__init__`

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

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_dataset.py#L160)

#### method `clear_dataset_cache`

```python
clear_dataset_cache()
```

Deletes the cached data for this specific datset

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_dataset.py#L61)

#### method `get_as_dict`

```python
get_as_dict(split: str = None, as_hdf5: bool = False)
```

Returns the data from the dataset as a dictionary

**Arguments:**

* `split` (string): Split to create dataset on.
* `**Default`: \*\* `None`

Returns: (dict) Dictionary of all the data from the specified split

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_dataset.py#L101)

#### method `get_as_tensorflow`

```python
get_as_tensorflow(split: str = None)
```

Convert Foundry Dataset to a Tensorflow Sequence

**Arguments:**

* `split` (string): Split to create Tensorflow Sequence on.
* `**Default`: \*\* `None`

Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_dataset.py#L81)

#### method `get_as_torch`

```python
get_as_torch(split: str = None)
```

Returns the data from the dataset as a TorchDataset

**Arguments:**

* `split` (string): Split to create PyTorch Dataset on.
* `**Default`: \*\* `None`

Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_dataset.py#L120)

#### method `get_citation`

```python
get_citation() → str
```

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_dataset.py#L136)

#### method `validate_metadata`

```python
validate_metadata(metadata)
```

Validate the JSON message against the FoundryDataset model

**Arguments:**

* `metadata` (dict): Metadata information provided by the user.

**Raises:**

* `ValidationError`: if metadata supplied by user does not meet the specificiation of a FoundryDataset object.

***

_This file was automatically generated via_ [_lazydocs_](https://github.com/ml-tooling/lazydocs)_._
