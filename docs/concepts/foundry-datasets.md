---
description: An introduction to how Foundry datasets and their metadata are defined
---

# Foundry Datasets

Foundry Datasets are comprised of two key components, [_**data**_](foundry-datasets.md#data) and descriptive [_**metadata**_](foundry-datasets.md#descriptive-metadata). In order to make the data easily consumable, _**data**_ (consisting of files) should be assembled following the supported structures. The _**metadata**_ description allows tracking of high level information (e.g.,  authors, associated institutions, licenses, data location), and also information on how to operate on the datasets (e.g., how to load the data, training/test splits).

## **Data**

### Example - Record-Based Data

#### **Tabular Data**

For tabular data, columns should represent the different keys of the data, and rows the individual records.

{% hint style="info" %}
Supported tabular data types currently include .json, .jsonl, and .csv
{% endhint %}

In this example, we showcase how to describe a JSON record-based dataset where each record is a valid JSON object in a JSON list or a line in a JSON line delimited file.

| **feature\_1** | **feature\_2** | **material\_type** | band\_gap |
| -------------- | -------------- | ------------------ | --------- |
| 0.10           | 0.52           | 1                  | 1.40      |
| 0.34           | 0.910          | 0                  | 0.73      |
| ...            | ...            | ...                |           |

For this example dataset, the `Key` Python object could be: &#x20;

```python
"keys": [{
	"key": "feature_1",
	"type": "input",
	"units": None,
	"description": "This is feature 1"
}, {
	"key": "feature_2",
	"type": "input",
	"units": None,
	"description": "This is feature 2"
}, {
	"key": "material_type",
	"type": "input",
	"units": None,
	"description": "This is the material type",
	"labels": ["perovskite", "not perovskite"]
} {
	"key": "band_gap",
	"type": "target",
	"units": "eV",
	"description": "This is the simulated band gap in eV"
}]
```

#### Hierarchical Data

Foundry also supports data from hierarchical data formats (e.g., [HDF5](https://www.h5py.org)). In this case, features and outputs can be represented with `/` notation. For example, if the features of a dataset are located in an array stored in `/data/arr1` and `/other_data/arr2` while the outputs are in `/data/labeled`, the `keys` list may contain the following `Key` objects:

```javascript
"keys": [{
		"key": ["/data/arr1"],
		"type": "input",
		"description": "input, unlabeled images"
	}, {
		"key": ["/data/arr2"],
		"type": "input",
		"description": "This is an another array containing input data"
	}, {
		"key": ["/data/labeled"],
		"type": "target",
		"description": "target, labeled images"
	}]
}
```

and the dataset may be described in whole as:

```python
{
	"short_name": "segmentation-dev",
	"data_type": "hdf5",
	"task_type": ["unsupervised", "segmentation"],
	"domain": ["materials science", "chemistry"],
	"n_items": 100,
	"splits": [{
		"type": "train",
		"path": "foundry.hdf5",
		"label": "train"
	}],
	"keys": [{
		"key": ["/data/arr1"],
		"type": "input",
		"description": "input, unlabeled images"
	}, {
		"key": ["/data/arr2"],
		"type": "input",
		"description": "This is an another array containing input data"
	}, {
		"key": ["/data/labeled"],
		"type": "target",
		"description": "target, labeled images"
	}]
}
```

## Descriptive Metadata

Metadata in Foundry comprehensively describe datasets using a combination of the DataCite metadata schema and our own Foundry schema.

### Metadata schema

**DataCite Metadata (object):** All datasets can be described using metadata in compliance with the [DataCite metadata format](https://schema.datacite.org). This metadata captures core elements needed for dataset citation and discovery, such as author names, institutions, associated abstracts, and more. Many of these capabilities have helper functions in the SDK, to make it easier to match the DataCite schema.

For a full list of the metadata keys in DataCite, see their [Metadata Schema 4.4 documentation](https://schema.datacite.org/meta/kernel-4.4/).

#### **Keys list (list of objects) \[required]:**&#x20;

`Key` objects provide a mapping that allows Foundry to read data from the underlying data structure into usable Python objects. `Key` objects have the following properties:

* **`key (str) [required]`**A name mapping to a column name (e.g., for csv files) or key within a data structure (e.g., for HDF5 files)
* **`type (str) [required]`** The type of key this entry represents. Currently suported types are _**\["input", "target" ]**_
* **`units (str)[optional]` **_****_ The scientific units associated with a key. _Default: None_
* **`description (str)[optional]` **_****_ A free text description of the key. _Default: None_
* **`labels (list) (str) [optional]`:** A list of strings mapped to integers in a key column

#### **splits (**list of objects**) \[required]:**

`split` objects provide a convenient way to specify various data splits, or subsets of the dataset. `split` objects have the following properties:

* **`type (str) [required]`**The type of split (e.g., "train", "test", "validation")
* **`path (str) [required]`** A path to the file or folder containing the split data
* **`label (str)` **_****_ A descriptive name for the split if required. _Default: None_

#### **short\_name (str) \[required]:**&#x20;

Short name is a unique, human-readable name associated with this dataset to make loading and finding the dataset simple.&#x20;

#### **data\_type (str) \[required]:**&#x20;

The type of data provided. This gives a hint to Foundry on how to map the keys into loading operations. _Options \["tabular","hdf5"]_

#### **task\_type (str)\[optional]:**

The type of process or analytical task the dataset is meant for. For example, "classification", "supervised", etc.

#### **domain (str)\[optional]:**

The science domain of the dataset. For example, "materials science".

#### **n\_items (number)\[optional]:**

The number of items within the dataset.

```
"foundry": {
	"dc": {},
	"keys": [{
			"type": "input",
			"name": "feature_1",
			"units": "",
			"description": "This is an input"
		},
		{
			"type": "target",
			"name": "band_gap",
			"units": "eV",
			"description": "blah blah",
			"labels": []
		}
	],
	"short_name": "my_short_name",
	"type": "tabular"
}
```

## Example usage

For loading datasets, see [Getting Started - Loading Data](../examples.md).

For a full example of exploring data using Foundry, see our [Jupyter notebook examples](https://github.com/MLMI2-CSSI/foundry/tree/main/examples).&#x20;
