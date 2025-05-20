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

{% hint style="success" %}
If you are running your script on cloud resources \(e.g. Google Colab, Binder\), see [Using Foundry on Cloud Computing Resources](examples.md#using-foundry-on-cloud-computing-resources)W
{% endhint %}

### Listing Datasets

To show all available Foundry datasets, you can use the Foundry `list()` method as follows. The method returns a pandas DataFrame with details on the available datasets.

```python
f.list()
```

### Loading Datasets

The Foundry client can be used to access datasets using their unique identifier (often a DOI or a specific `source_id`). You can find these identifiers by using the `f.list()` or `f.search("your query")` methods.

Let's load the metadata for a dataset. This example uses the `source_id` for the Fashion MNIST test dataset.
```python
from foundry import Foundry
f = Foundry() # Assumes default interactive authentication

# Search for the dataset
# Replace with a known DOI or source_id for a dataset you want to access
dataset_identifier = "_test_foundry_fashion_mnist_v1.1" 
results_df = f.search(dataset_identifier)

if results_df.empty:
    print(f"Dataset '{dataset_identifier}' not found.")
    dataset = None
else:
    # Get the FoundryDataset object
    dataset = results_df.iloc[0].FoundryDataset
    print(f"Found dataset: {dataset.dataset_name}")
    # In a Jupyter notebook, simply typing 'dataset' on its own line would display its metadata.
```

This will remotely load the dataset's metadata (e.g., data location, data keys, etc.). The actual data files are downloaded by the `FoundryCache` when you request the data if they are not already cached locally. By default, data is downloaded via Globus Transfer if `use_globus=True` (the default) and you have Globus Connect Personal set up. Otherwise, or if `use_globus=False`, it will use HTTPS.

Once you have the `dataset` object, you can load its data:
```python
if dataset:
    try:
        # Load the data. dataset.load() is an alias for dataset.get_as_dict()
        # This loads all splits by default. You can specify splits, e.g., dataset.load(split="train")
        data_splits = dataset.load() 
        
        # The structure of data_splits depends on the dataset.
        # For Fashion MNIST, it might look like:
        # {'train': {'input': <data>, 'output': <data>}, 'test': {'input': <data>, 'output': <data>}}
        
        if "train" in data_splits:
            X_train = data_splits['train']['input']
            y_train = data_splits['train']['output']
            print(f"Successfully loaded train data. X_train type: {type(X_train)}, y_train type: {type(y_train)}")
        else:
            print(f"No 'train' split found. Available splits: {list(data_splits.keys())}")
            
    except Exception as e:
        print(f"Error loading data for {dataset.dataset_name}: {e}")
```

The data are then usable within the variables like `X_train` and `y_train`. This full example can be found in [`/examples/fashion-mnist/`](https://github.com/MLMI2-CSSI/foundry/tree/master/examples/fashion-mnist) (Note: the example notebook there might also need updates to align with current API).

## Using Foundry on Cloud Computing Resources

Foundry works with common cloud computing providers \(e.g., the NSF sponsored Jetstream and Google Colab\). On these resources, simply add the following arguments to use a cloud-compatible authentication flow.

```python
f = Foundry(no_browser=True, no_local_server=True)
```

When downloading data (which happens when `dataset.load()` or similar methods are called), Foundry uses Globus by default. To use HTTPS instead (e.g., if Globus Connect Personal is not available or desired for transfers):

{% hint style="info" %}
This method may be slow for large datasets and datasets with many files
{% endhint %}

```python
# Initialize Foundry to use HTTPS for all data transfers
f = Foundry(use_globus=False, no_browser=True, no_local_server=True) 
# Then proceed with f.search(...) and dataset.load() as above.
# The dataset object created from this Foundry instance will inherit the use_globus=False setting.
```
Alternatively, if you have an existing `Foundry` instance `f` that was initialized with `use_globus=True`, creating a new one with `use_globus=False` is the way to switch to HTTPS for subsequent operations with datasets derived from that new instance. The `use_globus` preference is tied to the `FoundryCache` object, which is set up when `Foundry` is initialized.

