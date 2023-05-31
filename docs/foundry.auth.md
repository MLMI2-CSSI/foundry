<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/auth.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.auth`
Utilities related to storing authentication credentials 



---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/auth.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PubAuths`
Collection of the authorizers needed for publication 



**Attributes:**
 
 - <b>`transfer_client`</b>:  Client with credentials to perform transfers 
 - <b>`auth_client_openid`</b>:  Client with permissions to get users IDs 
 - <b>`endpoint_auth_clients`</b>:  Mapping between endpoint ID and client that can authorize access to it 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    transfer_client: TransferClient,
    auth_client_openid: AuthClient,
    endpoint_auth_clients: Dict[str, AuthClient]
) → None
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
