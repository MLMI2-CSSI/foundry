<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https_upload.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.https_upload`
Private utility methods to upload files and/or folders to Globus using HTTPS instead of Globus Transfer. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https_upload.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `upload_to_endpoint`

```python
upload_to_endpoint(
    auths: PubAuths,
    local_data_path: str,
    endpoint_id: str = '82f1b5c6-6e9b-11e5-ba47-22000b92c6ec',
    dest_parent: str = None,
    dest_child: str = None
) → Tuple[str, str]
```

Upload local data to a Globus endpoint using HTTPS PUT requests. Data can be a folder or an individual file. 

**Args:**
 
 - <b>`auths`</b> (PubAuths):  Dataclass of authorizers needed for upload. Includes `transfer_client`, `auth_client_openid`, 
 - <b>`and `endpoint_auth_clients`, which is a Dict of `endpoint_id``</b>: AuthClient mappings. 
 - <b>`local_data_path`</b> (str):  Path to the local dataset to publish to Foundry via HTTPS. Creates an HTTPS PUT  request to upload the data specified to a Globus endpoint (default is NCSA endpoint) before it is  transferred to MDF. 
 - <b>`endpoint_id`</b> (str):  Globus endpoint ID to upload the data to. Default is NCSA endpoint. Must match the  `endpoint_id` auth'd in `auths.auth_client_gcs`. 

Returns 
------- (str) Globus data source URL: URL pointing to the data on the Globus endpoint 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
