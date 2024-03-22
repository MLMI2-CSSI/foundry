# foundry.foundry\_cache

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L0)

## module `foundry.foundry_cache`

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L20)

### class `FoundryCache`

The FoundryCache manages the local storage of FoundryDataset objects

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L23)

#### method `__init__`

```python
__init__(forge_client: Forge, transfer_client: Any, local_cache_dir: str = None)
```

Initializes a FoundryCache object.

**Args:**

* `forge_client` (Forge): The Forge client object.
* `transfer_client` (Any): The transfer client object.
* `local_cache_dir` (str, optional): The local cache directory. Defaults to None. If not specified, defaults to either environmental variable ('FOUNDRY\_LOCAL\_CACHE\_DIR') or './data/'.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L461)

#### method `clear_cache`

```python
clear_cache(dataset_name: str = None)
```

Deletes all of the locally stored datasets

**Arguments:**

* `dataset_name` (str): Optional name of a specific dataset. If omitted, all datsets will be erased

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L44)

#### method `download_to_cache`

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

* `dataset_name` (str): Name of the dataset (equivalent to source\_id in MDF).
* `splits` (List\[FoundrySplit], optional): List of splits in the dataset. Defaults to None.
* `use_globus` (bool, optional): If True, use Globus to download the data; otherwise, try HTTPS. Defaults to False.
* `interval` (int, optional): How often to wait before checking Globus transfer status. Defaults to 10.
* `parallel_https` (int, optional): Number of files to download in parallel if using HTTPS. Defaults to 4.
* `verbose` (bool, optional): Produce more debug messages to screen. Defaults to False.
* `transfer_client` (Any, optional): The transfer client object. Defaults to None.

**Returns:**

* `FoundryCache`: The FoundryCache object.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L78)

#### method `download_via_globus`

```python
download_via_globus(dataset_name: str, interval: int)
```

Downloads selected dataset over Globus.

**Args:**

* `dataset_name` (str): Name of the dataset (equivalent to source\_id in MDF).
* `interval` (int): How often to wait before checking Globus transfer status.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L100)

#### method `download_via_http`

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

* `dataset_name` (str): Name of the dataset (equivalent to source\_id in MDF).
* `parallel_https` (int): Number of threads to use for downloading.
* `verbose` (bool): Produce more debug messages to screen.
* `transfer_client` (Any): The transfer client object.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L427)

#### method `get_keys`

```python
get_keys(
    foundry_schema: FoundrySchema,
    type: str = None,
    as_object: bool = False
)
```

Get keys for a Foundry dataset

**Arguments:**

* `foundry_schema` (FoundrySchema): The schema from MDF that contains the keys
* `type` (str): The type of key to be returned e.g., "input", "target"
* `as_object` (bool): When `False`, will return a list of keys in as strings When `True`, will return the full key objects
* `**Default`: \*\* `False` Returns: (list) String representations of keys or if `as_object` is False otherwise returns the full key objects.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L181)

#### method `load_as_dict`

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

* `dataset_name` (str): Name of the dataset (equivalent to source\_id in MDF).
* `foundry_schema` (FoundrySchema, optional): Schema element as obtained from MDF. Defaults to None.
* `use_globus` (bool, optional): If True, use Globus to download the data; otherwise, try HTTPS. Defaults to False.
* `interval` (int, optional): How often to wait before checking Globus transfer status. Defaults to 10.
* `parallel_https` (int, optional): Number of files to download in parallel if using HTTPS. Defaults to 4.
* `verbose` (bool, optional): Produce more debug messages to screen. Defaults to False.
* `transfer_client` (Any, optional): The transfer client object. Defaults to None.
* `as_hdf5` (bool, optional): If True and dataset is in HDF5 format, keep data in HDF5 format. Defaults to False.

**Returns:**

* `dict`: A labeled dictionary of tuples.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L270)

#### method `load_as_tensorflow`

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

* `split` (string): Split to create Tensorflow Sequence on.
* `**Default`: \*\* `None`

Returns: (TensorflowSequence) Tensorflow Sequence of all the data from the specified split

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L237)

#### method `load_as_torch`

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

* `split` (string): Split to create PyTorch Dataset on.
* `**Default`: \*\* `None`

Returns: (TorchDataset) PyTorch Dataset of all the data from the specified split

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry\_cache.py#L138)

#### method `validate_local_dataset_storage`

```python
validate_local_dataset_storage(
    dataset_name: str,
    splits: List[FoundrySplit] = None
)
```

Verifies that the local storage location exists and all expected files are present.

**Args:**

* `dataset_name` (str): Name of the dataset (equivalent to source\_id in MDF).
* `splits` (List\[FoundrySplit], optional): Labels of splits to be loaded. Defaults to None.

**Returns:**

* `bool`: True if the dataset exists and contains all the desired files; False otherwise.

***

_This file was automatically generated via_ [_lazydocs_](https://github.com/ml-tooling/lazydocs)_._
