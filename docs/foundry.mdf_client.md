<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.mdf_client`
Minimal MDF client replacing mdf_forge dependency. 

This provides the essential functionality needed by Foundry without requiring the full mdf_forge package. 

Also includes staging upload functionality for publishing local data to MDF without requiring Globus Connect Personal. 

**Global Variables**
---------------
- **STAGING_ENDPOINT_ID**
- **STAGING_BASE_PATH**
- **TRANSFER_API_BASE**
- **MDF_INDEX_ID**
- **MDF_TEST_INDEX_ID**


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `StagingUploader`
Handles uploading files to MDF staging endpoint. 

This allows users to publish local data to MDF without needing Globus Connect Personal running. Files are uploaded via HTTPS to a temporary staging location on the MDF public endpoint. 

Usage:  uploader = StagingUploader(transfer_token)  unique_id, remote_dir = uploader.create_staging_directory()  uploader.upload_file(Path("data.csv"), remote_dir)  # Then use globus://{STAGING_ENDPOINT_ID}{remote_dir}/ as data source 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(transfer_token: str, https_token: Optional[str] = None)
```

Initialize uploader with Globus tokens. 



**Args:**
 
 - <b>`transfer_token`</b>:  Globus OAuth2 access token with transfer scope 
 - <b>`https_token`</b>:  Globus OAuth2 access token with HTTPS scope for NCSA  (if None, uses transfer_token) 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_staging_directory`

```python
create_staging_directory() → tuple[str, str]
```

Create a unique directory on the staging endpoint. 



**Returns:**
  Tuple of (unique_id, full_path) for the created directory 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L166"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_globus_url`

```python
get_globus_url(remote_dir: str) → str
```

Get the Globus file manager URL for a staged directory. 

This is the format expected by MDF Connect for data sources. 



**Args:**
 
 - <b>`remote_dir`</b>:  Remote directory path (e.g., /tmp/uuid) 



**Returns:**
 Globus file manager URL for use with MDF 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `upload_directory`

```python
upload_directory(
    local_dir: Path,
    remote_dir: str,
    progress_callback=None
) → List[str]
```

Upload all files from a local directory. 



**Args:**
 
 - <b>`local_dir`</b>:  Local directory containing files to upload 
 - <b>`remote_dir`</b>:  Remote directory path 
 - <b>`progress_callback`</b>:  Optional callback(filename, current, total) 



**Returns:**
 List of remote paths to uploaded files 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `upload_file`

```python
upload_file(
    local_path: Path,
    remote_dir: str,
    filename: Optional[str] = None
) → str
```

Upload a single file to the staging endpoint via HTTPS. 



**Args:**
 
 - <b>`local_path`</b>:  Path to local file 
 - <b>`remote_dir`</b>:  Remote directory path (e.g., /tmp/uuid) 
 - <b>`filename`</b>:  Optional remote filename (defaults to local filename) 



**Returns:**
 Remote path to uploaded file 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MDFClient`
Minimal MDF client for dataset search and download. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L185"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    index: str = 'mdf',
    services: Optional[Any] = None,
    search_client: Optional[Any] = None,
    transfer_client: Optional[Any] = None,
    data_mdf_authorizer: Optional[Any] = None,
    petrel_authorizer: Optional[Any] = None
)
```

Initialize the MDF client. 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L307"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `globus_download`

```python
globus_download(
    results: List[Dict],
    dest: str = '.',
    dest_ep: Optional[str] = None,
    download_datasets: bool = True,
    **kwargs
) → Dict
```

Download data using Globus Transfer. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L247"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match_dois`

```python
match_dois(doi: str) → MDFClient
```

Filter by DOI. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L226"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match_organizations`

```python
match_organizations(organization: str) → MDFClient
```

Filter by organization. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match_resource_types`

```python
match_resource_types(resource_type: str) → MDFClient
```

Filter by resource type. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L231"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match_source_names`

```python
match_source_names(source_name: str) → MDFClient
```

Filter by source name or source ID. 



**Args:**
 
 - <b>`source_name`</b>:  The source_name or source_id of the dataset.  If a source_id is provided (e.g., 'dataset_v1.1'),  the version suffix is stripped automatically. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/mdf_client.py#L252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search`

```python
search(
    q: Optional[str] = None,
    advanced: bool = False,
    limit: int = 10,
    **kwargs
) → List[Dict]
```

Search for datasets. 



**Args:**
 
 - <b>`q`</b>:  Free-text search query 
 - <b>`advanced`</b>:  Force advanced query mode. Automatically enabled  when field-specific filters (DOI, source_name) are used. 
 - <b>`limit`</b>:  Maximum number of results to return 



**Returns:**
 List of dataset metadata dictionaries 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
