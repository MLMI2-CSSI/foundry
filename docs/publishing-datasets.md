---
description: Information on how to publish datasets
---

# Publishing Datasets

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
	"package_type": "files"
}
```



