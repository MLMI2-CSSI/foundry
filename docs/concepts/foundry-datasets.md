---
description: Describe the metadata that is for each Foundry dataset
---

# Foundry Datasets

Foundry Datasets are comprised of two key components, [_**data**_](foundry-datasets.md#data) and descriptive [_**metadata**_](foundry-datasets.md#describing-datasets-with-metadata). In order to make the data easily consumable, _**data**_ \(consisting of files\) should be assembled following the supported structures. The _**metadata**_ description allows tracking of high level information \(e.g.,  authors, assoicated institutions, licenses, data location\), and also information on how to operate on the datasets \(e.g., how to load the data, training/test splits\)

### **Data**

### Example - Record-Based Data

#### **Tabular Data**

For tabular data should, columns represent the different keys of the data, and rows represent individual records.

{% hint style="info" %}
Supported tabular data types currently include JSON, csv, and xlsx.
{% endhint %}

In this example, we showcase how to describe a JSON record-based dataset where each record is a valid JSON object in a JSON list or a line in a JSON line delimited file.

| **feature\_1** | **feature\_2** | **material\_type** | band\_gap |
| :--- | :--- | :--- | :--- |
| 0.10 | 0.52 | 1 | 1.40 |
| 0.34 | 0.910 | 0 | 0.73 |
| ... | ... | ... |  |

For this example dataset the `Key` object could be:  

```javascript
{
	"short_name": "oqmd-bandgaps",
	"data_type": "tabular",
	"task_type": ["supervised"],
	"domain": ["materials science"],
	"n_items": 29197,
	"splits": [{
		"type": "train",
		"path": "foundry_dataframe.json",
		"label": "train"
	}],
	"keys": [{
			"key": ["reference"],
			"type": "input",
			"units": "",
			"description": "source publication of the bandgap value"
		}, {
			"key": ["icsd_id"],
			"type": "input",
			"units": "",
			"description": "corresponding id in ICSD of this compound"
		}, {
			"key": ["structure"],
			"type": "input",
			"units": "",
			"description": "the structure of this compound"
		}, {
			"key": ["composition"],
			"type": "input",
			"units": "",
			"description": "reduced composition of this compound"
		}, {
			"key": ["comments"],
			"type": "input",
			"units": "",
			"description": "Additional information about this bandgap measurement"
		}, {
			"key": ["bandgap type"],
			"type": "input",
			"units": "",
			"description": "the type of the bandgap, e.g., direct or indirect"
		}, {
			"key": ["comp method"],
			"type": "input",
			"units": "",
			"description": "functional used to calculate the bandgap"
		}, {
			"key": ["space group"],
			"type": "input",
			"units": "",
			"description": "the space group of this compound"
		},
		{
			"key": ["bandgap value (eV)"],
			"type": "output",
			"units": "eV",
			"description": "value of the bandgap"
		}
	]
}
```

**TODO**

```text
"keys":[{
		 	"key": "feature_1",
			"type": "input",
			"units": None,
			"description": "This is feature 1"
		},{
			"key": "feature_2",
			"type": "input",
			"units": None,
			"description": "This is feature 2"
		},{
			"key": "material_type",
			"type": "input",
			"units": None,
			"description": "This is the material type",
			"labels":["perovskite","not perovskite"]
		}{
			"key": "band_gap",
			"type": "target",
			"units": "eV",
			"description": "This is the simulated band gap in eV"
		}
]
```

{% hint style="info" %}
`This tabular data file should be saved in the base directory as` **`foundry_dataframe.json`**
{% endhint %}

* Write general pandas reader to try csv, JSON, xlsx for opening

#### Hierarchical Data

Foundry also supports data from hierarchical data formats \(e.g., [HDF5](https://www.h5py.org)\). In this case features and outputs can be represented with `/` notation. For example, if the features of a dataset are located in an array stored in `/data/arr1` and `/other_data/arr2` while the outputs are in `/data/band_gaps`, the Key object would be:

```javascript
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
			"key": ["train/input"],
			"type": "input",
			"description": "input, unlabeled images"
		}, {
			"key": ["train/output"],
			"type": "target",
			"description": "target, labeled images"
		}]
	}
```

```text
"keys":[{
			"key": "/data/arr1",
			"type": "input",
			"units": None,
			"description": "This is an array containing input data"
		},{
		  "key": "/other_data/arr2",
			"type": "input",
			"units": None,
			"description": "This is an another array containing input data"
		},{
		  "key": "/data/band_gaps",
			"type": "target",
			"units": "eV",
			"description": "This is the simulated band gap in eV"
		}
]
```

## Descriptive Metadata

**DataCite Metadata \(object\):** All datasets can be described using metadata in compliance with the [DataCite metadata format](https://schema.datacite.org). This metadata captures . Many of these capabilities have helper functions in the SDK, to make it easier to match the DataCite schema

**Keys \(object\):** Key objects provide a mapping that allows Foundry to read data from the underlying data structure into usable Python objects. Key objects have the following properties

* **`key (str)`**A name mapping to a column name \(e.g., for csv files\) or key within a data structure \(e.g., for HDF5 files\)
* **`type (str)`** The type of key this entry represents. Currently suported types are _**\["input", "target" \]**_
* **`units (str)[optional]`** _****_The scientific units associated with a key. _Default: None_
* **`description (str)[optional]`** _****_A free text description of the key. _Default: None_
* **`labels (list) (str) [optional]`:** A list of strings mapped to integers in a key column

**short\_name \(str\):** Short name is a unique name associated with this dataset to make loading and . 

**type \(str\):** The type provides a hint to Foundry on how to map the keys into loading operations. _Options \["tabular","hdf5"\]_

```text
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

