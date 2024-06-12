---
description: Information on how to publish datasets
---

# Publishing Datasets

In order to publish datasets, the datasets must 1) adhere to specified Foundry dataset shapes ([see here](publishing-datasets.md#shaping-datasets)), and 2)  be described with required information ([see here](publishing-datasets.md#describing-datasets)). Together, the dataset shape and description enable researchers to reuse the datasets more easily.

{% hint style="info" %}
When datasets are published you will receive a [Digital Object Identifier (DOI) ](https://en.wikipedia.org/wiki/Digital\_object\_identifier)to enable citation of the research artifact
{% endhint %}

## Jupyter Notebook Publishing Guide

We created a notebook that walks you through the publication process. Just fill in the notebook with your data's details and you can publish right from there.

[Skip to the publication guide notebook.](../../examples/publishing-guides/dataset\_publishing.ipynb)

## Shaping Datasets

For a general dataset to be translated into a usable Foundry dataset, it should follow one of the prescribed shapes. It should also be described by a set of `Key` objects, which provides description of the data, and a mapping that allows Foundry to read data into usable Python objects ([see Describing Datasets](publishing-datasets.md#describing-datasets) for more info).&#x20;

### **Tabular Data**

Tabular data should be in a form where columns represent the different keys of the data and rows represent individual entries. For example:

| **feature\_1** | **feature\_2** | **material\_type** | band\_gap |
| -------------- | -------------- | ------------------ | --------- |
| 0.10           | 0.52           | 1                  | 1.40      |
| 0.34           | 0.910          | 0                  | 0.73      |
| ...            | ...            | ...                |           |

For this example dataset, the `keys` list could be: &#x20;

```python
"keys": [{
	"key": ["feature_1"],
	"type": "input",
	"units": "",
	"description": "This is feature 1"
},{
	"key": ["feature_2"],
	"type": "input",
	"units": "",
	"description": "This is feature 2"
},{
	"key": ["material_type"],
	"type": "input",
	"description": "This is the material type",
	"classes": ["perovskite", "not perovskite"]
},{
	"key": ["band_gap"],
	"type": "target",
	"units": "eV",
	"description": "This is the simulated band gap in eV"
}]
```

{% hint style="info" %}
`Don't forget to specify the tabular data filename and path in the submitted metadata. This can be done in a split - see the section on` [`Describing Datasets`](publishing-datasets.md#describing-datasets)
{% endhint %}

### Hierarchical Data

Foundry also supports data from hierarchical data formats (e.g., [HDF5](https://www.h5py.org)). In this case, features and outputs can be represented with `/` notation. For example, if the features of a dataset are located in an array stored in `/data/arr1` and `/other_data/arr2` while the outputs are in `/data/band_gaps`, the Key object would be:

```python
"keys": [{
	"key": ["/data/arr1"],
	"type": "input",
	"units": None,
	"description": "This is an array containing input data"
}, {
	"key": ["/other_data/arr2"],
	"type": "input",
	"units": None,
	"description": "This is an another array containing input data"
}, {
	"key": ["/data/band_gaps"],
	"type": "target",
	"units": "eV",
	"description": "This is the simulated band gap in eV"
}]
```

## Describing Datasets

**DataCite Metadata (object):** All datasets can be described using metadata in compliance with the [DataCite metadata format](https://schema.datacite.org). This metadata meets basic standards and adheres to uniform, consistent schema. Many of these capabilities have helper functions in the SDK, to make it easier to match the DataCite schema.

{% code fullWidth="false" %}
```python
example_datacite = {'identifier': {'identifier': '10.xx/xx', 'identifierType': 'DOI'},
                         'rightsList': [{'rights': 'CC-BY 4.0'}],
                         'creators': [{'creatorName': 'Brown, C', 'familyName': 'Brown', 'givenName': 'Charles'},
                                      {'creatorName': 'Van Pelt, L', 'familyName': 'Van Pelt', 'givenName': 'Lucia'}],
                         'subjects': [{'subject': 'blockheads'},
                                      {'subject': 'foundry'},
                                      {'subject': 'test_data'}],
                         'publicationYear': 2024,
                         'publisher': 'Materials Data Facility',
                         'dates': [{'date': '2024-08-03', 'dateType': 'Accepted'}],
                         'titles': [{'title': "You're a Good man, Charlie Brown"}],
                         'resourceType': {'resourceTypeGeneral': 'Dataset', 
                                          'resourceType': 'Dataset'}}
```
{% endcode %}

**Keys (list\[Key]):** `Key` objects provide a mapping that allows Foundry to read data from the underlying data structure into usable Python objects. Individual `Key` objects have the following properties

* **`key (str) [required]`**A name mapping to a column name (e.g., for csv files) or key within a data structure (e.g., for HDF5 files)
* **`type (str) [required]`** The type of key this entry represents. Currently suported types are _**\["input", "target" ]**_
* **`units (str)[optional]`** The scientific units associated with a key. _Default: None_
* **`description (str)[optional]`** A free text description of the key. _Default: None_
* **`labels (list) (str) [optional]`:** A list of strings mapped to integers in a key column

**Splits (list\[Split]) \[required]:** `Split`objects provide a way for users to specify which data should be included as test, train, or other user defined splits. Individual `Split` objects have the following properties

* **`type (str) [required]`**A split type, e.g., the Foundry special split types of `train`, `test`,  and`validation`. These special split types may be handled differently than custom split types defined by users.&#x20;
* **`path (str) [required]`** The full filepath to the dataset file or directory that contains the split
* **`label (str)`** A label to assign to this split

```python
"splits": [{
    "type": "train",
		"path": "g4mp2_data.json", # Specify the filename and path of the source file
		"label": "train"           # A text label for the split
}]
```

**short\_name (str) \[required]:** Short name is a unique name associated with this dataset to make loading and .&#x20;

**type (str) \[required]:** The type provides a hint to Foundry on how to map the keys into loading operations. _Options \["tabular","hdf5"]_

## Publishing

{% hint style="info" %}
Before continuing, be sure that you have 1) signed up for a [free Globus account](https://app.globus.org) and 2) [joined this Globus group](https://app.globus.org/groups/cc192dca-3751-11e8-90c1-0a7c735d220a/about).
{% endhint %}

Once your dataset is in the proper shape, and you have created the associated metadata structure, you can publish to Foundry! One example of a complete set of metadata to describe a dataset is shown below.

```python
example_metadata = {
    "short_name": "iris_example",
    "data_type": "tabular",
    'task_type': ['unsupervised', 'generative'],
    'domain': ['materials science', 'chemistry'],
    'n_items': 1000,
    'splits': [
        {'label': 'train', 'path': 'train.json', 'type': 'train'},
        {'label': 'test', 'path': 'test.json', 'type': 'test'}
    ],
    "keys":[
        {
            "key": ["sepal length (cm)"],
            "type": "input",
            "units": "cm",
            "description": "sepal length in unit(cm)"
        },
        {
            "key": ["sepal width (cm)"],
            "type": "input",
            "units": "cm",
            "description": "sepal width in unit(cm)"
        },
        {
            "key": ["petal length (cm)"],
            "type": "input",
            "units": "cm",
            "description": "petal length in unit(cm)"
        },
        {
            "key": ["petal width (cm)"],
            "type": "input",
            "units": "cm",
            "description": "petal width in unit(cm)"
        },
        {
            "key": ["y"],
            "type": "output",
            "units": "",
            "description": "flower type",
            "classes": [
                {
                    "label": "0",
                    "name": "setosa"
                },
                {
                    "label": "1",
                    "name": "versicolor"
                },
                {
                    "label": "2",
                    "name": "virginica"
                }
            ]
        }
    ],    
}
```



## Publishing

Now that we have the metadata and datacite information contained in the json objects we created above, we can create an instance of a FoundryDataset object. This serves as a container to hold and organize all of the data as well as the metadata for the dataset. We just need one additional bit of information: a `dataset name` that we can use to reference the dataset.

```python
from foundry import FoundryDataset

dataset_name = 'charlies_iris_dataset'

iris_dataset = FoundryDataset(dataset_name=dataset_name, 
                              datacite_entry=example_iris_datacite,
                              foundry_schema=example_iris_metadata)




```

If your metadata is correct, you'll receive this message:

```
Datacite validation successful.
FoundrySchema validation successful.
```

Now that we have a `FoundryDataset` object instantiated, we need to give it some data! To do so we call the `add_data()` method on the `FoundryDataset` instance, and pass it a keyword argument `local_data_path` that references a path to a local file or folder that contains the data we want to publish.

```python
# path to the data for HTTPS upload
# NOTE: if uploading via Globus Connect Client, you'll want to specify `globus_data_source` instead 

data_path = "./data/iris.csv"
iris_dataset.add_data(local_data_path=data_path)
```

To publish, we call the `publish_dataset()` method on our `foundry` object, and provide it with our `FoundryDataset.`

```python
# publish to Foundry! returns a result object we can inspect
res = f.publish_dataset(iris_dataset)
```

```python
# check if publication request was valid
res['success']

#This will return `True` if successful
```

We can inspect the entire `res` object for more detailed information about the publication. For the above publication, `res` would have the format:

```python
{'source_id': 'charlies_iris_dataset',
 'success': True,
 'error': None,
 'status_code': 202}
```

Note that for large datasets, or for datasets that you would like to upload faster than HTTPS allows, you can create a Globus Transfer. Instead of specifying `https_data_path`, use `globus_data_source`:

<pre><code># Globus endpoint URL where your dataset is located
<strong>globus_data_source = "https://app.globus.org/file-manager?origin_id=e38ee745-6d04-11e5-ba46-22000b92c6ec&#x26;origin_path=%2Ffoundry%2F_test_blaiszik_foundry_bandgap_v1.2%2F"
</strong></code></pre>

More information about how to get the Globus source URL to the dataset you would like to publish can be found in our [Publishing Guide](../../examples/publishing-guides/dataset\_publishing.ipynb).

{% hint style="success" %}
Once the dataset is submitted, there is a manual curation step required to maintain dataset standards. This will take additional time.
{% endhint %}

## When will my data be available in Foundry?

When you submit your dataset, it will be transferred to the Foundry data store and then any necessary metadata will be extracted for making your dataset searchable.

It then enters a human curation phase, where our team checks that the contents are safe and properly formatted; please note that curation can take **up to a day or longer** around weekends and holidays.

We we can use the `source_id` of the `res` result to check the status of our submission. Ths `source_id` is a unique identifier based on the title and version of your data package.

```python
source_id = res['source_id']
f.check_status(source_id=source_id)
```

## Updating or republishing a dataset <a href="#updating-or-republishing-a-data-package" id="updating-or-republishing-a-data-package"></a>

To re-publish a dataset, pass `update=True` to `f.publish()`

```python
# republishing same dataset -- note the version increments automatically
res = f.publish_dataset(ds, update=True)
res
```
