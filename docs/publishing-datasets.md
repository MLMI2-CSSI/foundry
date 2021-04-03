---
description: Information on how to publish datasets
---

# Publishing Datasets

In order to publish datasets, the datasets must 1\) adhere to specified Foundry dataset shapes \([see here](publishing-datasets.md#shaping-datasets)\), and 2\)  be described with required information \([see here](publishing-datasets.md#describing-datasets)\). Together, the dataset shape and description enable researchers to reuse the datasets more easily.

## Examples

[Skip to the publication example notebook.](https://github.com/MLMI2-CSSI/foundry/blob/master/examples/foundry_publication_example.ipynb)

## Shaping Datasets

For a general dataset to be translated into a usable Foundry dataset, it should follow one of the prescribed shapes. It should also be described by a Key object, which provides a mapping that allows Foundry to read data from the underlying data structure into usable Python objects \([see Describing Datasets](publishing-datasets.md#describing-datasets) for more info\). 

### **Tabular Data**

Tabular data should include in a form where columns represent the different keys of the data and rows represent individual entries.

| **feature\_1** | **feature\_2** | **material\_type** | band\_gap |
| :--- | :--- | :--- | :--- |
| 0.10 | 0.52 | 1 | 1.40 |
| 0.34 | 0.910 | 0 | 0.73 |
| ... | ... | ... |  |

For this example dataset the `Key` object could be:  

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

### Hierarchical Data

Foundry also supports data from hierarchical data formats \(e.g., [HDF5](https://www.h5py.org)\). In this case features and outputs can be represented with `/` notation. For example, if the features of a dataset are located in an array stored in `/data/arr1` and `/other_data/arr2` while the outputs are in `/data/band_gaps`, the Key object would be:

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

## Describing Datasets

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

## Publishing

{% hint style="info" %}
Before continuing, be sure that you have 1\) signed up for a [free Globus account](https://app.globus.org) and 2\) [joined this Globus group](https://app.globus.org/groups/cc192dca-3751-11e8-90c1-0a7c735d220a/about).
{% endhint %}

Once your dataset is in the proper shape, and you have created the associated metadata structure, you can publish to Foundry!

Currently, you can publish any dataset you have stored on a Globus endpoint or Google Drive. In the following, assume your [previously defined metadata](publishing-datasets.md#describing-datasets) are stored in `metadata` :

```python
from foundry import Foundry

# Globus endpoint URL where your dataset is located
data_source = "https://app.globus.org/file-manager?origin_id=e38ee745-6d04-11e5-ba46-22000b92c6ec&origin_path=%2Ffoundry%2F_test_blaiszik_foundry_iris_v1.2%2F"

# full title of dataset
title = "Scourtas example iris dataset"

# authors to list 
authors = ["A Scourtas", "B Blaiszik"]

# shorthand title (optional)
short_name = "example_AS_iris"

# affiliations of authors (optional)
affiliations = ["Globus Labs, UChicago"]

# publisher of the data (optional)
publisher = "Materials Data Facility"

# publication year (optional)
publication_year = 2021


f = Foundry()
res = f.publish(metadata, data_source, title, authors, short_name=short_name))
```

The `publish()` method returns a result object that you can inspect for information about the state of the publication. For the above publication, `res` would have the format:

```python
{'error': None,
 'source_id': '_test_example_iris_v1.1',
 'status_code': 202,
 'success': True}
```



## Future Work

* Add support for wildcard key type specifications
* Add link to example publication

