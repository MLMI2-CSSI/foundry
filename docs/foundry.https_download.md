<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https_download.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.https_download`
Methods to download files from a Globus endpoint 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https_download.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `recursive_ls`

```python
recursive_ls(tc: TransferClient, ep: str, path: str, max_depth: int = 3)
```

Find all files in a Globus directory recursively 



**Args:**
 
 - <b>`tc`</b>:  TransferClient authorized to access the directory 
 - <b>`ep`</b>:  Endpoint on which the files reside 
 - <b>`path`</b>:  Path to the files being downloaded 
 - <b>`max_depth`</b>:  Maximum recurse depth 



**Yields:**
 Dictionaries describing the location of the files. Each includes at least 
 - <b>`"name"`</b>:  Name of the file 
 - <b>`"path"`</b>:  Absolute path to the file's location 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https_download.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download_file`

```python
download_file(item, base_directory, https_config, timeout=1800)
```

Download a file to disk 



**Args:**
 
 - <b>`item`</b>:  Dictionary defining the path to the file 
 - <b>`base_directory`</b>:  Base directory for storing downloaded files 
 - <b>`https_config`</b>:  Configuration defining the URL of the server and the name of the dataset 
 - <b>`timeout`</b>:  Timeout for the download request in seconds (default: 1800) 



**Returns:**
 
 - <b>`str`</b>:  Path to the downloaded file 



**Raises:**
 
 - <b>`DownloadError`</b>:  If the download fails for any reason 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https_download.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DownloadError`
Raised when a file download fails. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https_download.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(url: str, reason: str, destination: str = None)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
