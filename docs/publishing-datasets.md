---
description: Information on how to publish datasets
---

# Publishing Datasets

## [Skip to Publication Example Notebook](https://github.com/MLMI2-CSSI/foundry/blob/master/examples/foundry_publication_example.ipynb)

## Shaping Datasets

For a general dataset to be translated into a usable Foundry dataset, it should follow one of the prescribed shapes.

**Tabular Data**

Tabular data should include in a form where columns represent the different keys of the data and rows represent individual entries.

| **feature\_1** | **feature\_2** | **band\_gap** |
| :--- | :--- | :--- |
| 0.10 | 0.52 | 1.40 |
| 0.34 | 0.91 | 0.73 |
| ... | ... | ... |

For this example dataset the keys list would be:  

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

Foundry also supports of data from hierarchical data formats \(e.g., HDF5\). In this case features and outputs can be represented with `/` notation. For example, if the features of a dataset are located in an array stored in `/data/arr1` and `/other_data/arr2` while the outputs are in `/data/band_gaps`

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
* **`units (str)[optional]`** _****The scientific units associated with a key. Default: None_
* **`description (str)[optional]`** _****A free text description of the key. Default: None_

**short\_name \(str\):** Short name is a unique name associated with this dataset to make loading and . 

**type \(str\):** The type provides a hint to Foundry on how to map the keys into loading operations. _Options \["tabular","hdf5"\]_

```text
"foundry": {
	"dc": {},
	"keys": [{
			"type": "input",
			"name": "*",
			"units": "",
			"description": "These are the inputs"
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



## Future Work

* Add support for wildcard key type specifications
* Add link to example publication

