<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.foundry`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Foundry`
Foundry Client Base Class 

**TODO:**
 
------- Add Docstring 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    no_browser=False,
    no_local_server=False,
    index='mdf',
    authorizers=None,
    globus=True,
    verbose=False,
    interval=10,
    **data
)
```

Initialize a Foundry client 

**Args:**
 
 - <b>`no_browser`</b> (bool):   Whether to open the browser for the Globus Auth URL. 
 - <b>`no_local_server`</b> (bool):  Whether a local server is available.  This should be `False` when on remote server (e.g., Google Colab ). 
 - <b>`index`</b> (str):  Index to use for search and data publication. Choices `mdf` or `mdf-test` 
 - <b>`authorizers`</b> (dict):  A dictionary of authorizers to use, following the `mdf_toolbox` format 
 - <b>`globus`</b> (bool):  If True, download using Globus, otherwise https 
 - <b>`verbose`</b> (bool):  If True print additional debug information 
 - <b>`interval`</b> (int):  How often to poll Globus to check if transfers are complete 
 - <b>`data`</b> (dict):  Other arguments, e.g., results from an MDF search result that are used  to populate Foundry metadata fields 



**Returns:**
 an initialized and authenticated Foundry client 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L378"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `dataset_from_metadata`

```python
dataset_from_metadata(metadata: dict) → FoundryDataset
```

Converts the result of a forge query to a FoundryDatset object 



**Args:**
 
 - <b>`metadata`</b> (dict):  result from a forge query 



**Returns:**
 
 - <b>`FoundryDataset`</b>:  a FoundryDataset object created from the metadata 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L203"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_dataset_by_name`

```python
get_dataset_by_name(name: str) → FoundryDataset
```

Query foundry datasets by name 

Name is equivalent of 'source_id' in MDF. Should only return a single result. 



**Args:**
 
 - <b>`doi`</b> (str):  doi of desired datset 



**Returns:**
 
 - <b>`FoundryDataset`</b>:  a FoundryDatset object for the result of the query 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L407"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L222"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_metadata_by_doi`

```python
get_metadata_by_doi(doi: str) → dict
```

Query foundry datasets by DOI 

Should only return a single result. 



**Args:**
 
 - <b>`doi`</b> (str):  doi of desired datset 



**Returns:**
 
 - <b>`metadata`</b> (dict):  result from a forge query 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L241"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_metadata_by_query`

```python
get_metadata_by_query(q: str, limit: int) → dict
```

Submit query to forge client and return results 



**Args:**
 
 - <b>`q`</b> (str):  query string 
 - <b>`limit`</b> (int):  maximum number of results to return 



**Returns:**
 
 - <b>`metadata`</b> (dict):  result from a forge query 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list(limit: int = None)
```

List available Foundry datasets 



**Args:**
 
 - <b>`limit`</b> (int):  maximum number of results to return 

Returns 
 - <b>`List[FoundryDataset]`</b>:  List of FoundryDatset objects 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L260"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L352"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search`

```python
search(query: str = None, limit: int = None) → [<class 'FoundryDataset'>]
```

Search available Foundry datasets 



**Args:**
 
 - <b>`query`</b> (str):  query string to match 
 - <b>`limit`</b> (int):  maximum number of results to return 



**Returns:**
 
 - <b>`List[FoundryDataset]`</b>:  List of search results as FoundryDatset objects 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
