<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.foundry`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Foundry`
Foundry Client Base Class 

**TODO:**
 
------- Add Docstring 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    no_browser=False,
    no_local_server=False,
    index='mdf',
    authorizers=None,
    **data
)
```

Initialize a Foundry client 

**Args:**
 
 - <b>`no_browser`</b> (bool):   Whether to open the browser for the Globus Auth URL. 
 - <b>`no_local_server`</b> (bool):  Whether a local server is available.  This should be `False` when on remote server (e.g., Google Colab ). 
 - <b>`index`</b> (str):  Index to use for search and data publication. Choices `mdf` or `mdf-test` 
 - <b>`authorizers`</b> (dict):  A dictionary of authorizers to use, following the `mdf_toolbox` format 
 - <b>`data`</b> (dict):  Other arguments, e.g., results from an MDF search result that are used  to populate Foundry metadata fields 

Returns 
------- an initialized and authenticated Foundry client 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L452"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `check_status`

```python
check_status(source_id, short=False, raw=False)
```

Check the status of your submission. 



**Arguments:**
 
 - <b>`source_id`</b> (str):  The ``source_id`` (``source_name`` + version information) of the  submission to check. Returned in the ``res`` result from ``publish()`` via MDF Connect Client. 
 - <b>`short`</b> (bool):  When ``False``, will print a status summary containing  all of the status steps for the dataset.  When ``True``, will print a short finished/processing message,  useful for checking many datasets' status at once. 
 - <b>`**Default`</b>: ** ``False`` 
 - <b>`raw`</b> (bool):  When ``False``, will print a nicely-formatted status summary.  When ``True``, will return the full status result.  For direct human consumption, ``False`` is recommended. 
 - <b>`**Default`</b>: ** ``False`` 



**Returns:**
 
 - <b>`If ``raw`` is ``True``, *dict*`</b>:  The full status result. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L481"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `configure`

```python
configure(**kwargs)
```

Set Foundry config Keyword Args:  file (str): Path to the file containing  (default: self.config.metadata_file) 

dataframe_file (str): filename for the dataframe file default:"foundry_dataframe.json" data_file (str): : filename for the data file default:"foundry.hdf5" destination_endpoint (str): Globus endpoint UUID where Foundry data should move local_cache_dir (str): Where to place collected data default:"./data" 

Returns 
------- (Foundry): self: for chaining 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L499"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download`

```python
download(
    globus: bool = True,
    interval: int = 20,
    parallel_https: int = 4,
    verbose: bool = False
) → Foundry
```

Download a Foundry dataset 



**Args:**
 
 - <b>`globus`</b>:  if True, use Globus to download the data else try HTTPS 
 - <b>`interval`</b>:  How often to wait before checking Globus transfer status 
 - <b>`parallel_https`</b>:  Number of files to download in parallel if using HTTPS 
 - <b>`verbose`</b>:  Produce more debug messages to screen 



**Returns:**
 self, for chaining 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L321"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_citation`

```python
get_citation() → str
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L595"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_keys`

```python
get_keys(type=None, as_object=False)
```

Get keys for a Foundry dataset 



**Arguments:**
 
 - <b>`type`</b> (str):  The type of key to be returned e.g., "input", "target" 
 - <b>`as_object`</b> (bool):  When ``False``, will return a list of keys in as strings  When ``True``, will return the full key objects 
 - <b>`**Default`</b>: ** ``False`` Returns: (list) String representations of keys or if ``as_object`` is False otherwise returns the full key objects. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L246"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list()
```

List available Foundry datasets Returns 
-------  (pandas.DataFrame): DataFrame with summary list of Foundry datasets including name, title, publication year, and DOI 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L151"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load`

```python
load(
    name,
    download=True,
    globus=False,
    verbose=False,
    metadata=None,
    authorizers=None,
    **kwargs
)
```

Load the metadata for a Foundry dataset into the client 

**Args:**
 
 - <b>`name`</b> (str):  Name of the foundry dataset 
 - <b>`download`</b> (bool):  If True, download the data associated with the package (default is True) 
 - <b>`globus`</b> (bool):  If True, download using Globus, otherwise https 
 - <b>`verbose`</b> (bool):  If True print additional debug information 
 - <b>`metadata`</b> (dict):  **For debug purposes.** A search result analog to prepopulate metadata. 

Keyword Args: 
 - <b>`interval`</b> (int):  How often to poll Globus to check if transfers are complete 

Returns 
------- self 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L270"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_data`

```python
load_data(source_id=None, globus=True, as_hdf5=False)
```

Load in the data associated with the prescribed dataset 

Tabular Data Type: Data are arranged in a standard data frame stored in self.dataframe_file. The contents are read, and 

File Data Type: <<Add desc>> 

For more complicated data structures, users should subclass Foundry and override the load_data function 



**Args:**
 
 - <b>`inputs`</b> (list):  List of strings for input columns 
 - <b>`targets`</b> (list):  List of strings for output columns 
 - <b>`source_id`</b> (string):  Relative path to the source file 
 - <b>`as_hdf5`</b> (bool):  If True and dataset is in hdf5 format, keep data in hdf5 format 

Returns 
------- 
 - <b>`(tuple)`</b>:  Tuple of X, y values 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L337"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `publish_dataset`

```python
publish_dataset(
    foundry_metadata: Dict[str, Any],
    title: str,
    authors: List[str],
    https_data_path: str = None,
    globus_data_source: str = None,
    update: bool = False,
    publication_year: int = None,
    test: bool = False,
    **kwargs: Dict[str, Any]
) → Dict[str, Any]
```

Submit a dataset for publication; can choose to submit via HTTPS using `https_data_path` or via Globus  Transfer using the `globus_data_source` argument. Only one upload method may be specified. 

**Args:**
 
 - <b>`foundry_metadata`</b> (dict):  Dict of metadata describing data package 
 - <b>`title`</b> (string):  Title of data package 
 - <b>`authors`</b> (list):  List of data package author names e.g., Jack Black  or Nunez, Victoria 
 - <b>`https_data_path`</b> (str):  Path to the local dataset to publish to Foundry via HTTPS. Creates an HTTPS PUT  request to upload the data specified to a Globus endpoint (default is NCSA endpoint) before it is  transferred to MDF. If None, the user must specify a 'globus_data_source' URL to the location of the  data on their own Globus endpoint. User must choose either `globus_data_source` or `https_data_path` to  publish their data. 
 - <b>`globus_data_source`</b> (str):  Url path for a data folder on a Globus endpoint; url can be obtained through  the Globus Web UI or SDK. If None, the user must specify an 'https_data_path' pointing to the location  of the data on their local machine. User must choose either `globus_data_source` or `https_data_path` to  publish their data. 
 - <b>`update`</b> (bool):  True if this is an update to a prior data package 
 - <b>`(default`</b>:  self.config.metadata_file) 
 - <b>`publication_year`</b> (int):  Year of dataset publication. If None, will  be set to the current calendar year by MDF Connect Client. 
 - <b>`(default`</b>:  $current_year) 
 - <b>`test`</b> (bool):  If True, do not submit the dataset for publication (ie transfer to the MDF endpoint).  Default is False. 

Keyword Args: 
 - <b>`affiliations`</b> (list):  List of author affiliations 
 - <b>`tags`</b> (list):  List of tags to apply to the data package 
 - <b>`short_name`</b> (string):  Shortened/abbreviated name of the data package 
 - <b>`publisher`</b> (string):  Data publishing entity (e.g. MDF, Zenodo, etc.) 
 - <b>`description`</b> (str):  A description of the dataset. 
 - <b>`dataset_doi`</b> (str):  The DOI for this dataset (not an associated paper). 
 - <b>`related_dois`</b> (list):  DOIs related to this dataset,  not including the dataset's own DOI (for example, an associated paper's DOI). 

Returns 
------- (dict) MDF Connect Response: Response from MDF Connect to allow tracking of dataset. Contains `source_id`, which can be used to check the status of the submission 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L426"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `publish_model`

```python
publish_model(
    title,
    creators,
    short_name,
    servable_type,
    serv_options,
    affiliations=None,
    paper_doi=None
)
```

Simplified publishing method for servables 



**Args:**
 
 - <b>`title`</b> (string):  title for the servable 
 - <b>`creators`</b> (string | list):  either the creator's name (FamilyName, GivenName) or a list of the creators' names 
 - <b>`short_name`</b> (string):  shorthand name for the servable 
 - <b>`servable_type`</b> (string):  the type of the servable, must be a member of ("static_method",  "class_method",  "keras",  "pytorch",  "tensorflow",  "sklearn") 
 - <b>`serv_options`</b> (dict):  the servable_type specific arguments that are necessary for publishing. arguments can be found at 
 - <b>`https`</b>: //dlhub-sdk.readthedocs.io/en/latest/source/dlhub_sdk.models.servables.html under the appropriate ``create_model`` signature. use the argument names as keys and their values as the values. 
 - <b>`affiliations`</b> (list):  list of affiliations for each author 
 - <b>`paper_doi`</b> (str):  DOI of a paper that describes the servable 

**Returns:**
 
 - <b>`(string)`</b>:  task id of this submission, can be used to check for success 

**Raises:**
 
 - <b>`ValueError`</b>:  If the given servable_type is not in the list of acceptable types 
 - <b>`Exception`</b>:  If the serv_options are incomplete or the request to publish results in an error 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L254"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(name, inputs, funcx_endpoint=None, **kwargs)
```

Run a model on data 



**Args:**
 
 - <b>`name`</b> (str):  DLHub model name 
 - <b>`inputs`</b>:  Data to send to DLHub as inputs (should be JSON serializable) 
 - <b>`funcx_endpoint`</b> (optional):  UUID for the funcx endpoint to run the model on, if not the default (eg River) 

Returns 
-------  Returns results after invocation via the DLHub service 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L216"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search`

```python
search(q=None, limit=None)
```

Search available Foundry datasets q (str): query string to match limit (int): maximum number of results to return 

Returns 
-------  (pandas.DataFrame): DataFrame with summary list of Foundry data packages including name, title, publication year, and DOI 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L749"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L734"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
