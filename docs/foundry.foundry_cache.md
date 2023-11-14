<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.foundry_cache`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryCache`
The FoundryCache manages the local storage of FoundryDataset objects 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_cache`

```python
clear_cache()
```

Deletes all of the locally stored datasets 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `dataset_present`

```python
dataset_present(dataset: FoundryDataset)
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_to_cache`

```python
download_to_cache(
    dataset: FoundryDataset,
    globus: bool = True,
    interval: int = 20,
    parallel_https: int = 4,
    verbose: bool = False
)
```

Downloads the data from source to local storage 



**Args:**
 
 - <b>`dataset`</b>:  a FoundryDataset object created from the metadata 
 - <b>`globus`</b>:  if True, use Globus to download the data else try HTTPS 
 - <b>`interval`</b>:  How often to wait before checking Globus transfer status 
 - <b>`parallel_https`</b>:  Number of files to download in parallel if using HTTPS 
 - <b>`verbose`</b>:  Produce more debug messages to screen 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_via_http`

```python
download_via_http(dataset: FoundryDataset, parallel_https: int, verbose: bool)
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry_cache.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `validate_local_storage`

```python
validate_local_storage(dataset: FoundryDataset)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
