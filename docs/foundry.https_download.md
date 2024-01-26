<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https_download.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.https_download`
Methods to download files from a Globus endpoint 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https_download.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https_download.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download_file`

```python
download_file(item, data_directory, https_config)
```

Download a file to disk 



**Args:**
 
 - <b>`item`</b>:  Dictionary defining the path to the file 
 - <b>`https_config`</b>:  Configuration defining the URL of the server and the name of the dataset 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
