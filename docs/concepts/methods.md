# Methods

## Introduction

The most important Foundry methods are listed below. Full documentation coming soon.

In the following examples, assume `f = Foundry()`

### Methods

#### .load()

`f.load(dataset, download, globus)`: The `dataset` can be the desired dataset's `short_name` / `source_id` or `doi`. `download` and `globus`are boolean values. Set `globus` to True if you are using a Globus endpoint. This method returns the datasets [metadata](foundry-datasets.md#descriptive-metadata).

#### .load\_data()

`f.load_data()`: This method loads the data into the client and returns a DataFrame object.

#### .list()

`f.list()`:  The method returns a pandas DataFrame with details on the available datasets with their source\_id, name, publishing year, and DOI.

![Table returned by f.list() of all datasets in the MDF index](<../.gitbook/assets/Screen Shot 2022-01-27 at 1.29.23 PM (1).png>)
