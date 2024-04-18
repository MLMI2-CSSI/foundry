---
description: We'll take you from importing Foundry all the way to seeing your data.
---

# Using Datasets

## Scientific Examples

We have [example notebooks](https://github.com/MLMI2-CSSI/foundry/tree/main/examples) using material science data that illustrate how to load data or publish datasets using Foundry. These notebooks are compatible with Google Colab and with Jupyter Notebook. However, some of the datasets are quite large and cannot be loaded into Google Colab without the pro version.

## Quickstart

### Creating a Foundry Client

The Foundry client provides access to all of the methods described here for listing, loading, and publishing datasets and models. The code below will create a Foundry client&#x20;

```python
from foundry import Foundry
f = Foundry()
```

{% hint style="success" %}
If you are running your script on cloud resources (e.g. Google Colab, Binder), see: [Using Foundry on Cloud Computing Resources](examples.md#using-foundry-on-cloud-computing-resources)
{% endhint %}

### Listing Datasets

To show all available Foundry datasets, you can use the Foundry [`list()` method](../classes-and-methods/foundry.foundry.md) as follows. The method returns a pandas DataFrame with details on the available datasets.

```python
f.list()
```

![The returned Dataframe from f.list()](<../.gitbook/assets/Screen Shot 2022-01-27 at 1.29.23 PM.png>)

### Searching Datasets

The Foundry client can be used to search for datasets using a `source_id` or a digital object identifier (DOI) e.g. here `"foundry_wei_atom_locating_benchmark"` or `"10.18126/e73h-3w6n"`_._ You can retrieve the `source_id`from the [`list()` method](examples.md#listing-datasets).

```python
from foundry import Foundry

f = Foundry()

dataset_doi = '10.18126/e73h-3w6n'
datasets = f.search(dataset_doi)
```

The search method will return a list of `FoundryDataset` objects. If searching by DOI, you can expect that it will be the first result and select that `FoundryDataset` object by specifying the first index.

```
dataset = datasets[0]
```

### Finding Datasets

Instead of using `search`, you can use the `get_dataset_by_name()` or `get_dataset_by_doi()` methods. Both methods return a FoundryDataset associated with the given name or DOI.

```
from foundry import Foundry

f = Foundry()

dataset_doi = '10.18126/e73h-3w6n'
dataset = f.get_dataset_by_doi(dataset_doi)
```

### Loading Datasets

To load the dataset, you can use the `get_as_dict()` method appended to the `FoundryDataset` object. From the example above, this looks like:

```
dataset.get_as_dict()
```

This will remotely load the metadata (e.g., data location, data keys, etc.) and download the data to local storage if it is not already cached.&#x20;

{% hint style="success" %}
All datasets are accessible via HTTPS and Globus by authenticated download. HTTPS is the default. Read about the [FoundryDataset object](../classes-and-methods/foundry.foundry\_dataset.md) to use Globus.
{% endhint %}

To learn more about the dataset, you can access the metadata.&#x20;

<pre><code><strong>f.get_metadata_by_doi('10.18126/e73h-3w6n')
</strong></code></pre>

The image below is what `get_metadata_by_doi()` looks like when printed in a notebook. This table contains the dataset's [metadata](../publishing/describing-datasets.md#descriptive-metadata).

![](<../.gitbook/assets/image (4).png>)

This is an example of accessing data in a specified [split](../publishing/describing-datasets.md#splits) that is defined for the dataset, here we use `train`.&#x20;

```python
imgs = dataset['train']['input']['imgs']
coords = dataset['train']['input']['coords']


# Show some images with coordinate overlays
import matplotlib.pyplot as plt

n_images = 3
offset = 150
key_list = list(res['train']['input']['imgs'].keys())[0+offset:n_images+offset]

fig, axs = plt.subplots(1, n_images, figsize=(20,20))
for i in range(n_images):
    axs[i].imshow(imgs[key_list[i]])
    axs[i].scatter(coords[key_list[i]][:,0], 
                   coords[key_list[i]][:,1], s = 20, c = 'r', alpha=0.5)
```

![Overlay of a STEM image with atomic coordinate labels (red dots)](<../.gitbook/assets/image (1).png>)

## Using Foundry on Cloud Computing Resources

Foundry works with common cloud computing providers (e.g., the NSF sponsored Jetstream and Google Colab). On these resources, simply add the following arguments to use a cloud-compatible authentication flow.

```python
f = Foundry(no_browser=True, no_local_server=True)
```

