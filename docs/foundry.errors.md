<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.errors`
Structured error classes for Foundry. 

These errors provide: 1. Error codes for programmatic handling 2. Human-readable messages 3. Recovery hints for agents and users 4. Structured details for debugging 

This enables both humans and AI agents to understand and recover from errors. 



---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryError`
Base error class with structured information for agents and users. 



**Attributes:**
 
 - <b>`code`</b>:  Machine-readable error code (e.g., "DATASET_NOT_FOUND") 
 - <b>`message`</b>:  Human-readable error description 
 - <b>`details`</b>:  Additional context for debugging 
 - <b>`recovery_hint`</b>:  Actionable suggestion for resolving the error 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    code: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    recovery_hint: Optional[str] = None
) → None
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → Dict[str, Any]
```

Serialize error to dictionary for JSON responses. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DatasetNotFoundError`
Raised when a dataset cannot be found. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(query: str, search_type: str = 'query')
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → Dict[str, Any]
```

Serialize error to dictionary for JSON responses. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AuthenticationError`
Raised when authentication fails. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(service: str, reason: str = None)
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → Dict[str, Any]
```

Serialize error to dictionary for JSON responses. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DownloadError`
Raised when a file download fails. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(url: str, reason: str, destination: str = None)
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → Dict[str, Any]
```

Serialize error to dictionary for JSON responses. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DataLoadError`
Raised when loading data from a file fails. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(file_path: str, reason: str, data_type: str = None)
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → Dict[str, Any]
```

Serialize error to dictionary for JSON responses. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ValidationError`
Raised when metadata validation fails. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(field_name: str, error_msg: str, schema_type: str = 'metadata')
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → Dict[str, Any]
```

Serialize error to dictionary for JSON responses. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PublishError`
Raised when publishing a dataset fails. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L132"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(reason: str, source_id: str = None, status: str = None)
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → Dict[str, Any]
```

Serialize error to dictionary for JSON responses. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CacheError`
Raised when cache operations fail. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L147"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(operation: str, reason: str, cache_path: str = None)
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → Dict[str, Any]
```

Serialize error to dictionary for JSON responses. 


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L159"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ConfigurationError`
Raised when Foundry is misconfigured. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(setting: str, reason: str, current_value: Any = None)
```








---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/errors.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → Dict[str, Any]
```

Serialize error to dictionary for JSON responses. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
