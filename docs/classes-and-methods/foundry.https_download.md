# foundry.https\_download

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https\_download.py#L0)

## module `foundry.https_download`

Methods to download files from a Globus endpoint

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https\_download.py#L12)

### function `recursive_ls`

```python
recursive_ls(tc: TransferClient, ep: str, path: str, max_depth: int = 3)
```

Find all files in a Globus directory recursively

**Args:**

* `tc`: TransferClient authorized to access the directory
* `ep`: Endpoint on which the files reside
* `path`: Path to the files being downloaded
* `max_depth`: Maximum recurse depth

**Yields:** Dictionaries describing the location of the files. Each includes at least

* `"name"`: Name of the file
* `"path"`: Absolute path to the file's location

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https\_download.py#L56)

### function `download_file`

```python
download_file(item, data_directory, https_config)
```

Download a file to disk

**Args:**

* `item`: Dictionary defining the path to the file
* `https_config`: Configuration defining the URL of the server and the name of the dataset

***

_This file was automatically generated via_ [_lazydocs_](https://github.com/ml-tooling/lazydocs)_._
