<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/integrations/huggingface.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.integrations.huggingface`
Hugging Face Hub integration for Foundry datasets. 

This module provides functionality to export Foundry datasets to Hugging Face Hub, making materials science datasets discoverable in the broader ML ecosystem. 

Requirements:  pip install foundry-ml[huggingface] 

Usage:  from foundry import Foundry  from foundry.integrations.huggingface import push_to_hub 

 f = Foundry()  dataset = f.get_dataset("10.18126/abc123")  push_to_hub(dataset, "materials-science/bandgap-data") 

**Global Variables**
---------------
- **HF_AVAILABLE**

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/integrations/huggingface.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `push_to_hub`

```python
push_to_hub(
    dataset,
    repo_id: str,
    token: Optional[str] = None,
    private: bool = False,
    split: Optional[str] = None
) → str
```

Export a Foundry dataset to Hugging Face Hub. 

This creates a new dataset repository on HF Hub with the Foundry data, automatically generating a Dataset Card from the DataCite metadata. 



**Args:**
 
 - <b>`dataset`</b>:  A FoundryDataset object (from foundry.get_dataset()) 
 - <b>`repo_id`</b>:  HF Hub repository ID (e.g., "materials-science/bandgap-data") 
 - <b>`token`</b>:  HuggingFace API token. If None, uses cached credentials. 
 - <b>`private`</b>:  If True, create a private repository. 
 - <b>`split`</b>:  Specific split to export. If None, exports all splits. 



**Returns:**
 
 - <b>`str`</b>:  URL of the created dataset on HF Hub. 



**Example:**
 ``` from foundry import Foundry```
    >>> from foundry.integrations.huggingface import push_to_hub
    >>> f = Foundry()
    >>> ds = f.get_dataset("10.18126/abc123")
    >>> url = push_to_hub(ds, "my-org/my-dataset")
    >>> print(f"Dataset published at: {url}")





---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
