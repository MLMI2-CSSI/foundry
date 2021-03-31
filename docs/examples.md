# Getting Started with Python

## Scientific Examples

[Checkout our example notebooks ](https://github.com/MLMI2-CSSI/foundry/tree/master/examples)for how to load or publish datasets using Foundry.

## Quickstart

### Creating a Foundry Client

The Foundry client provides access to all of the methods described here for listing, loading, and publishing datasets and models. The code below will create a Foundry client 

```python
from foundry import Foundry
f = Foundry()
```

If you are running your script on cloud resources \(e.g. Google Colab, Binder\), you can use the following:

```python
from foundry import Foundry
f = Foundry(no_browser=True, no_local_server=True)
```

### Listing Datasets

To show all available Foundry datasets, you can use the Foundry `list()` method as follows. The method returns a pandas DataFrame with details on the available datasets.

```python
f.list()
```

### Loading Datasets

The Foundry client can be used to access datasets using a `source_id`, e.g. here "\_test\_foundry\_fashion\_mnist_v1.1"._ You can retrieve the `source_id` from the [`list()` method](examples.md#listing-datasets).

```python
from foundry import Foundry
f = Foundry()
f = f.load("_test_foundry_fashion_mnist_v1.1")
```

This will remotely load the metadata \(e.g., data location, data keys, etc.\) and download the data to local storage if it is not already cached. Data can be downloaded via HTTPS without additional setup or more optimally with a Globus endpoint [set up](https://www.globus.org/globus-connect-personal) on your machine.

Once the data are accessible locally, access the data with the `load_data()` method.

```python
X, y = f.load_data()
```

The data are then usable within the `X` and `y` variables. This full example can be found in [`/examples/fashion-mnist/`](https://github.com/MLMI2-CSSI/foundry/tree/master/examples/fashion-mnist).

## Using Foundry on Cloud Computing Resources

Foundry works with common cloud computing providers \(e.g., the NSF sponsored Jetstream and Google Colab\). On these resources, simply add the following arguments to use a cloud-compatible authentication flow.

```python
f = Foundry(no_browser=True, no_local_server=True)
```

When downloading data, add the following argument to download via HTTPS.

{% hint style="info" %}
This method may be slow for large datasets and datasets with many files
{% endhint %}

```python
f.download(globus=False)
```

