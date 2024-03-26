# foundry.auth

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/auth.py#L0)

## module `foundry.auth`

Utilities related to storing authentication credentials

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/auth.py#L9)

### class `PubAuths`

Collection of the authorizers needed for publication

**Attributes:**

* `transfer_client`: Client with credentials to perform transfers
* `auth_client_openid`: Client with permissions to get users IDs
* `endpoint_auth_clients`: Mapping between endpoint ID and client that can authorize access to it

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/%3Cstring%3E)

#### method `__init__`

```python
__init__(
    transfer_client: TransferClient,
    auth_client_openid: AuthClient,
    endpoint_auth_clients: Dict[str, AuthClient]
) → None
```

***

_This file was automatically generated via_ [_lazydocs_](https://github.com/ml-tooling/lazydocs)_._
