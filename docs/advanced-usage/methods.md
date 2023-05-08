# Methods

## Introduction

The most important Foundry methods are listed below. Full documentation coming soon.

In the following examples, assume `f = Foundry()`

### Methods

#### Foundry()

`f = Foundry()`

Initialize a Foundry client

**Args:**

`no_browser (bool)`: Whether to open the browser for the Globus Auth URL.

`no_local_server (bool)`: Whether a local server is available. his should be `False` when  on remote server (e.g., Google Colab ).

`index (str)`: Index to use for search and data publication. Choices `mdf` or `mdf-test`

`authorizers (dict)`: A dictionary of authorizers to use, following the `mdf_toolbox` format

`data (dict)`: Other arguments, e.g., results from an MDF search result that are used to populate Foundry metadata fields

**Returns** an initialized and authenticated Foundry client



#### .load()

`f.load(dataset, download, globus)`:&#x20;

Load the metadata for a Foundry dataset into the client.

**Args:**

`name (str)`: Name of the foundry dataset

`download (bool)`: If True, download the data associated with the package (default is True)

`globus (bool)`: If True, download using Globus, otherwise https

`verbose (bool)`: If True print additional debug information

`metadata (dict)`: **For debug purposes.** A search result analog to prepopulate metadata.

**Keyword Args:**

`interval (int)`: How often to poll Globus to check if transfers are complete

**Returns** the dataset's [metadata](../publishing/describing-datasets.md#descriptive-metadata).



#### .load\_data()

`f.load_data()`

Load in the data associated with the prescribed dataset

**Args:**

`inputs (list)`: List of strings for input columns

`targets (list)`: List of strings for output columns

**Returns** (tuple): Tuple of X, y values



#### .list()

`f.list()`:

List available Foundry data packages

**Returns** (pandas.DataFrame): DataFrame with summary list of Foundry data packages including name, title, and publication year

![Table returned by f.list() of all datasets in the MDF index](<../.gitbook/assets/Screen Shot 2022-01-27 at 1.29.23 PM (1).png>)

####

#### get\_packages()

`get_packages():`

Get available local data packages

**Args:**

`paths (bool)`: If True return paths in addition to package, if False return package name only

**Returns** (list): List describing local Foundry packages



#### collect\_dataframes()

`collect_dataframes`:

Collect dataframes of local data packages

**Args:**

`packages (list)`: List of packages to collect, defaults to all

**Returns** (tuple): Tuple of X(pandas.DataFrame), y(pandas.DataFrame)



#### publish\_dataset()

`publish_dataset()`:

Submit a dataset for publication; can choose to submit via HTTPS using `https_data_path` or via Globus Transfer using the `globus_data_source` argument. Only one upload method may be specified.

**Args:**

`foundry_metadata (dict)`: Dict of metadata describing data package

`title (string):` Title of data package

`authors (list)`: List of data package author names e.g., Jack Black or Nunez, Victoria

`https_data_path (string)`: Path to the local dataset to publish to Foundry via HTTPS. Creates an HTTPS PUT request to upload the data specified to a Globus endpoint (default is NCSA endpoint) before it is transferred to MDF. If None, the user must specify a `globus_data_source` URL to the location of the data on their own Globus endpoint. User must choose either `globus_data_source` or `https_data_path` to publish their data.

`globus_data_source (string)` : Url path for a data folder on a Globus endpoint; url can be obtained through the Globus Web UI or SDK. If None, the user must specify an `https_data_path` pointing to the location of the data on their local machine. User must choose either `globus_data_source` or `https_data_path` to publish their data.

`update (bool)`: True if this is an update to a prior data package (default: self.config.metadata\_file)

`publication_year (int)`: Year of dataset publication. If None, will be set to the current calendar year by MDF Connect Client. (default: $current\_year)

`test (bool)` : If True, do not submit the dataset for publication (ie transfer to the MDF endpoint). Default is False.

**Keyword Args:**

`affiliations (list)`: List of author affiliations

`tags (list)`: List of tags to apply to the data package

`short_name (string):` Shortened/abbreviated name of the data package

`publisher (string)`: Data publishing entity (e.g. MDF, Zenodo, etc.)

`description (str)`: A description of the dataset.

`dataset_doi (str)`: The DOI for this dataset (not an associated paper).

`related_dois (list)`: DOIs related to this dataset, not including the dataset's own DOI (for example, an associated paper's DOI).

**Returns** (dict) MDF Connect Response: Response from MDF Connect to allow tracking of dataset. Contains `source_id`, which can be used to check the status of the submission



#### check\_status()

`check_status()`:

Check the status of your submission.

**Args:**

`source_id (str):` The `source_id` (`source_name` + version information) of the submission to check. Returned in the `res` result from `publish()` via MDF Connect Client.

`short (bool)`: When `False`, will print a status summary containing all of the status steps for the dataset. When `True`, will print a short finished/processing message, useful for checking many datasets' status at once. **Default:** `False`

`raw (bool)`: When `False`, will print a nicely-formatted status summary. When `True`, will return the full status result. For direct human consumption, `False` is recommended. **Default:** `False`

**Returns** _dict_: The full status result if `raw` is `True`



#### **configure()**

`configure()`:

Set Foundry config

**Keyword Args:**

`file (str)`: Path to the file containing (default: self.config.metadata\_file)

`dataframe_file (str)`: filename for the dataframe file default:"foundry\_dataframe.json"

`data_file (str)`: filename for the data file default:"foundry.hdf5"

`destination_endpoint (str)`: Globus endpoint UUID where Foundry data should move

`local_cache_dir (str)`: Where to place collected data default:"./data"

**Returns** (Foundry): self: for chaining



#### download()

`download()`:

Download a Foundry dataset

**Args:**

`globus (bool)`: if True, use Globus to download the data else try HTTPS

`verbose (bool)`: if True print out debug information during the download

**Returns** (Foundry): self: for chaining



#### build()

`build()`:

Build a Foundry Data Package

**Args:**

`spec (multiple)`: dict or str (relative filename) of the data package specification

`globus (bool)`: if True use Globus to fetch datasets

`interval (int)`: Polling interval on checking task status in seconds.

`type (str)`: One of "file" or None

**Returns** (Foundry): self: for chaining





#### get\_keys()

`get_keys():`

Get keys for a Foundry dataset

**Args:**

`type (str)`: The type of key to be returned e.g., "input", "target"

`as_object (bool)`: When `False`, will return a list of keys in as strings. When `True`, will return the full key objects. **Default:** `False`

**Returns** (list) String representations of keys or if `as_object` is False otherwise returns the full key objects.
