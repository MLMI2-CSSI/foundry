---
description: We'll take you from importing Foundry all the way to seeing your data.
---

# Getting Started Loading Data

## Scientific Examples

We have [example notebooks](https://github.com/MLMI2-CSSI/foundry/tree/main/examples) using material science data that illustrate how to load data or publish datasets using Foundry. These notebooks are compatible with Google Colab and with Jupyter Notebook. However, some of the datasets are quite large and cannot be loaded into Google Colab without the pro version.

## Quickstart

### Creating a Foundry Client

The Foundry client provides access to all of the methods described here for listing, loading, and publishing datasets and models. The code below will create a Foundry client&#x20;

```python
from foundry import Foundry
f = Foundry(index="mdf")
```

{% hint style="success" %}
If you are running your script on cloud resources (e.g. Google Colab, Binder), see: [Using Foundry on Cloud Computing Resources](examples.md#using-foundry-on-cloud-computing-resources)
{% endhint %}

### Listing Datasets

To show all available Foundry datasets, you can use the Foundry [`list()` method](concepts/methods.md#.list) as follows. The method returns a pandas DataFrame with details on the available datasets.

```python
f.list()
```

![The returned Dataframe from f.list()](<.gitbook/assets/Screen Shot 2022-01-27 at 1.29.23 PM (1).png>)

### Loading Datasets

The Foundry client can be used to access datasets using a `source_id` or a digital object identifier (DOI) e.g. here `"foundry_wei_atom_locating_benchmark"` or `"10.18126/e73h-3w6n"`_._ You can retrieve the `source_id`from the [`list()` method](examples.md#listing-datasets).

```python
from foundry import Foundry

f = Foundry(index="mdf")
f.load("10.18126/e73h-3w6n", globus=True)
```

The [`load()` method](concepts/methods.md#.load) will remotely load the metadata (e.g., data location, data keys, etc.) and download the data to local storage if it is not already cached. Data can be downloaded via HTTPS without additional setup (set `download` to `True` and `globus` to `False`) or more optimally with a Globus endpoint [set up](https://www.globus.org/globus-connect-personal) on your machine (set `download` to `False` and `globus` to `True`).&#x20;

The image below is what `f` looks like when printed in a notebook. This table contains the dataset's [metadata](concepts/foundry-datasets.md#descriptive-metadata).

![](../.gitbook/assets/image.png)

Once the data are accessible locally, access the data with the [`load_data()` method](concepts/methods.md#.load\_data). Load data allows you to load data from a specific [split](concepts/foundry-datasets.md#splits) that is defined for the dataset, here we use `train`.&#x20;

```python
res = f.load_data()
imgs = res['train']['input']['imgs']
coords = res['train']['input']['coords']


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
f = Foundry(index="mdf", no_browser=True, no_local_server=True)
```

When downloading data, add the following argument to download via HTTPS.

{% hint style="info" %}
This method may be slow for large datasets and datasets with many files
{% endhint %}

```python
f.load("10.18126/e73h-3w6n", download=True, globus=False)
data = f.load_data()
```

