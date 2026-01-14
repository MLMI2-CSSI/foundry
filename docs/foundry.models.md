<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.models`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundrySpecificationDataset`
Pydantic base class for datasets within the Foundry data package specification 


---

#### <kbd>property</kbd> model_extra

Get extra fields set during validation. 



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`. 

---

#### <kbd>property</kbd> model_fields_set

Returns the set of fields that have been explicitly set on this model instance. 



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults. 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundrySpecification`
Pydantic base class for interacting with the Foundry data package specification The specification provides a way to group datasets and manage versions 


---

#### <kbd>property</kbd> model_extra

Get extra fields set during validation. 



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`. 

---

#### <kbd>property</kbd> model_fields_set

Returns the set of fields that have been explicitly set on this model instance. 



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults. 



---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_dependency`

```python
add_dependency(name: str, version: str)
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_dependencies`

```python
clear_dependencies()
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `model_dump`

```python
model_dump()
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `remove_duplicate_dependencies`

```python
remove_duplicate_dependencies()
```






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryDatasetType`
Foundry Dataset Types Enumeration of the possible Foundry dataset types 





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundrySchema`
A model for the Foundry schema based on the FoundryModel (project_model.py) class. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(project_dict: Dict[str, Any])
```






---

#### <kbd>property</kbd> model_extra

Get extra fields set during validation. 



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`. 

---

#### <kbd>property</kbd> model_fields_set

Returns the set of fields that have been explicitly set on this model instance. 



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults. 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryDatacite`
A model for the Datacite schema based on the Datacite (dc_model.py) class. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(datacite_dict: Dict[str, Any], **kwargs)
```






---

#### <kbd>property</kbd> model_extra

Get extra fields set during validation. 



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`. 

---

#### <kbd>property</kbd> model_fields_set

Returns the set of fields that have been explicitly set on this model instance. 



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults. 




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FoundryBase`
Configuration information for Foundry instance 


---

#### <kbd>property</kbd> model_extra

Get extra fields set during validation. 



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`. 

---

#### <kbd>property</kbd> model_fields_set

Returns the set of fields that have been explicitly set on this model instance. 



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults. 



---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/models.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `model_dump`

```python
model_dump()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
