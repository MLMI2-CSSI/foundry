---
description: Information on how to publish datasets
---

# Publishing Datasets

In order to publish datasets, the datasets must 1\) adhere to specified Foundry dataset shapes \([see here](publishing-datasets.md#shaping-datasets)\), and 2\)  be described with required information \([see here](publishing-datasets.md#describing-datasets)\). Together, the dataset shape and description enable researchers to reuse the datasets more easily.

## Examples

[Skip to the publication example notebook.](https://github.com/MLMI2-CSSI/foundry/blob/master/examples/foundry_publication_example.ipynb)

## Shaping Datasets

For a general dataset to be translated into a usable Foundry dataset, it should follow one of the prescribed shapes. It should also be described by a `Key` object, which provides a mapping that allows Foundry to read data from the underlying data structure into usable Python objects \([see Describing Datasets](publishing-datasets.md#describing-datasets) for more info\). 

### **Tabular Data**

Tabular data should include in a form where columns represent the different keys of the data and rows represent individual entries.

| **feature\_1** | **feature\_2** | **material\_type** | band\_gap |
| :--- | :--- | :--- | :--- |
| 0.10 | 0.52 | 1 | 1.40 |
| 0.34 | 0.910 | 0 | 0.73 |
| ... | ... | ... |  |

For this example dataset the `keys` list could be:  

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
`Don't forget to specify the tabular data file in the submitted metadata`
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

**Keys \(list\[Key\]\):** `Key` objects provide a mapping that allows Foundry to read data from the underlying data structure into usable Python objects. Individual `Key` objects have the following properties

* **`key (str)`**A name mapping to a column name \(e.g., for csv files\) or key within a data structure \(e.g., for HDF5 files\)
* **`type (str)`** The type of key this entry represents. Currently suported types are _**\["input", "target" \]**_
* **`units (str)[optional]`** _****_The scientific units associated with a key. _Default: None_
* **`description (str)[optional]`** _****_A free text description of the key. _Default: None_
* **`labels (list) (str) [optional]`:** A list of strings mapped to integers in a key column

**Splits \(list\[Split\]\):** `Split`objects provide a way for users to specify which data should be included as test, train, or other user defined splits. Individual `Split` objects have the following properties

* **`type (str)`**A name mapping to a column name \(e.g., for csv files\) or key within a data structure \(e.g., for HDF5 files\)
* **`path (str)`** The full filepath to the dataset file or directory that contains the split
* **`label (str)`** A label to assign to this split

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
	"data_type": "tabular"
}
```

## Publishing

{% hint style="info" %}
Before continuing, be sure that you have 1\) signed up for a [free Globus account](https://app.globus.org) and 2\) [joined this Globus group](https://app.globus.org/groups/cc192dca-3751-11e8-90c1-0a7c735d220a/about).
{% endhint %}

Once your dataset is in the proper shape, and you have created the associated metadata structure, you can publish to Foundry! An example is shown below.

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
	"data_type": "tabular"
}
```

Currently, you can publish datasets stored locally on your machine or on a Globus endpoint.

To publish a dataset, you first need to create a `FoundryDataset` object, which encapsulates your dataset's metadata and data location.

**1. Prepare Your Metadata:**

   You'll need two main pieces of metadata, typically as Python dictionaries:
   *   **DataCite Metadata (`datacite_entry`):** This dictionary should conform to the [DataCite schema](https://schema.datacite.org) and include information like titles, creators, publisher, publication year, etc.
       ```python
       # Example DataCite dictionary
       datacite_entry = {
           "titles": [{"title": "My Awesome Materials Dataset"}],
           "creators": [{"creatorName": "Doe, Jane", "affiliations": ["University of Science"]}],
           "publisher": "My Research Group",
           "publicationYear": "2023",
           "identifier": { # Optional: If you already have a DOI, include it
               "identifier": "10.1234/mydataset",
               "identifierType": "DOI"
           },
           "subjects": [{"subject": "materials science"}, {"subject": "machine learning"}]
           # Add other required and optional DataCite fields as needed
       }
       ```
   *   **Foundry Schema (`foundry_schema`):** This dictionary describes how Foundry should interpret your dataset, including splits (e.g., train, test), input/output specifications, data types, etc.
       ```python
       # Example Foundry schema dictionary
       foundry_schema = {
           "dataset_name": "my_awesome_dataset_v1", # Choose a unique name for your dataset
           "data_type": "tabular", # or "hdf5", "files", "other"
           "splits": [
               {"label": "train", "path": "data/train.csv", "type": "tabular"},
               {"label": "test", "path": "data/test.csv", "type": "tabular"}
           ],
           "inputs": ["feature1", "feature2"],
           "outputs": ["target_property"],
           # ... other fields like 'input_details', 'output_details' as needed
       }
       ```
       **Important:** The `dataset_name` in `foundry_schema` will be used as the `source_id` for your dataset in MDF. It should be unique.

**2. Create a `FoundryDataset` Object:**

   ```python
   from foundry import FoundryDataset

   try:
       dataset_to_publish = FoundryDataset(
           dataset_name=foundry_schema["dataset_name"], # Must match the one in foundry_schema
           datacite_entry=datacite_entry,
           foundry_schema=foundry_schema
       )
   except Exception as e: # Catches Pydantic ValidationError or other issues
       print(f"Error creating FoundryDataset: {e}")
       # Handle error appropriately
   ```

**3. Add Your Data Source:**

   Specify where your actual data files are located. You have two options:

   *   **Local Data (`local_data_path`):** If your data is on your local machine. Foundry will upload it to a temporary Globus endpoint location before transferring it to MDF.
       ```python
       dataset_to_publish.add_data(local_data_path="/path/to/your/dataset_folder_or_file")
       ```
   *   **Globus Endpoint (`globus_data_source`):** If your data is already on a Globus endpoint that you own or have access to. Provide the Globus URL to the data folder.
       ```python
       globus_url = "globus://<your_endpoint_id>/path/to/your_data/"
       dataset_to_publish.add_data(globus_data_source=globus_url)
       ```
       You can obtain this URL from the Globus Web UI by navigating to your data and copying the path from the "Path" field, then prepending `globus://<your_endpoint_id>`.

**4. Publish the Dataset:**

   ```python
   from foundry import Foundry

   f = Foundry() # Initialize Foundry client
   try:
       res = f.publish_dataset(foundry_dataset=dataset_to_publish)
       # To publish as an update to an existing dataset (ensure dataset_name matches):
       # res = f.publish_dataset(foundry_dataset=dataset_to_publish, update=True)
       
       # To test the publication process without actually submitting to MDF:
       # res = f.publish_dataset(foundry_dataset=dataset_to_publish, test=True)
       
       if res and res.get('success'):
           print(f"Dataset publication submitted successfully!")
           print(f"Source ID: {res.get('source_id')}") # Use this to check status
       else:
           print(f"Dataset publication failed. Response: {res}")
           
   except Exception as e:
       print(f"An error occurred during publication: {e}")
   ```

The `publish_dataset()` method returns a result object that you can inspect for information about the state of the publication. For a successful submission, `res` would typically have the format:

```python
{'error': None,
 'source_id': '_test_example_iris_v1.1',
 'status_code': 202,
 'success': True}
```



## Future Work

* Add support for wildcard key type specifications
* Add link to example publication

