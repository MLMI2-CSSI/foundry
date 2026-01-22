<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/integrations/__init__.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.integrations`
Foundry integrations with external platforms. 

This module provides bridges to other data ecosystems: 
- Hugging Face Hub: Export datasets to HF for broader visibility 

Usage:  from foundry.integrations.huggingface import push_to_hub 

 # Export a Foundry dataset to Hugging Face  dataset = foundry.get_dataset("10.18126/abc123")  push_to_hub(dataset, "my-org/dataset-name") 

**Global Variables**
---------------
- **huggingface**




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
