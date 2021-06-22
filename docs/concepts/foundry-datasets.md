---
description: Describe the metadata that is for each Foundry dataset
---

# Foundry Datasets

Foundry Datasets are comprised of two key components, data and descriptive metadata. In order to make the data easily consumable, data \(consisting of files\) should be assembled following the supported structures. The metadata description allows tracking of high level information \(e.g.,  authors, assoicated institutions, licenses, data location\), and also information on how to operate on the datasets \(e.g., how to load the data, training/test splits\)

## Data

### Example - Record-Based Data

{% hint style="info" %}
Supported tabular data types currently include JSON, csv, and xlsx.
{% endhint %}

In this example, we showcase how to describe a JSON record-based dataset where each record is a valid JSON object in a JSON list or a line in a JSON line delimited file.

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

* Write general pandas reader to try csv, JSON, xlsx for opening

### Example - Images Stored in HDF5 Format

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

## Example - Image Data in Folders

Not yet supported





