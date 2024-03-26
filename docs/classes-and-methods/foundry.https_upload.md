# foundry.https\_upload

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https\_upload.py#L0)

## module `foundry.https_upload`

Private utility methods to upload files and/or folders to Globus using HTTPS instead of Globus Transfer.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/https\_upload.py#L19)

### function `upload_to_endpoint`

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

* `auths` (PubAuths): Dataclass of authorizers needed for upload. Includes `transfer_client`, `auth_client_openid`,
* `and` endpoint\_auth\_clients`, which is a Dict of` endpoint\_id\`\`: AuthClient mappings.
* `local_data_path` (str): Path to the local dataset to publish to Foundry via HTTPS. Creates an HTTPS PUT request to upload the data specified to a Globus endpoint (default is NCSA endpoint) before it is transferred to MDF.
* `endpoint_id` (str): Globus endpoint ID to upload the data to. Default is NCSA endpoint. Must match the `endpoint_id` auth'd in `auths.auth_client_gcs`.

Returns ------- (str) Globus data source URL: URL pointing to the data on the Globus endpoint

***

_This file was automatically generated via_ [_lazydocs_](https://github.com/ml-tooling/lazydocs)_._
