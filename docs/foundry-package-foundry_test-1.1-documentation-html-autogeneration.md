# foundry package — Foundry\_test 1.1 documentation - HTML AUTOGENERATION

## foundry.foundry module[¶](broken-reference)

&#x20;_class_ foundry.foundry.Foundry(_no\_browser=False_, _no\_local\_server=False_, _search\_index='mdf-test'_, _\*_, _dc: Dict = {}_, _mdf: Dict = {}_, _dataset:_ [_foundry.models.FoundryDataset_](broken-reference) _= {}_, _config:_ [_foundry.models.FoundryConfig_](broken-reference) _= FoundryConfig(dataframe\_file='foundry\_dataframe.json', data\_file='foundry.hdf5', metadata\_file='foundry\_metadata.json', destination\_endpoint=None, local=False, metadata\_key='foundry', organization='foundry', local\_cache\_dir='./data')_, _dlhub\_client: Any = None_, _forge\_client: Any = None_, _connect\_client: Any = None_, _xtract\_tokens: Any = None_)[¶](broken-reference)

Bases: [`foundry.models.FoundryMetadata`](broken-reference)

Foundry Client Base Class TODO: ——- Add Docstring build(_spec_, _globus=False_, _interval=3_, _file=False_)[¶](broken-reference)

Build a Foundry Data Package :param spec: dict or str (relative filename) of the data package specification :type spec: multiple :param globus: if True use Globus to fetch datasets :type globus: bool :param interval: Polling interval on checking task status in seconds. :type interval: int :param type: One of “file” or None :type type: strReturns

**(Foundry)**Return type

self: for chaining check\_model\_status(_res_)[¶](broken-reference)

Check status of model or function publication to DLHub

TODO: currently broken on DLHub side of things check\_status(_source\_id_, _short=False_, _raw=False_)[¶](broken-reference)

Check the status of your submission.Parameters

* **source\_id** (_str_) – The `source_id` (`source_name` + version information) of the submission to check. Returned in the `res` result from `publish()` via MDF Connect Client.
* **short** (_bool_) – When `False`, will print a status summary containing all of the status steps for the dataset. When `True`, will print a short finished/processing message, useful for checking many datasets’ status at once. **Default:** `False`
* **raw** (_bool_) – When `False`, will print a nicely-formatted status summary. When `True`, will return the full status result. For direct human consumption, `False` is recommended. **Default:** `False`

Returns

The full status result.Return type

If `raw` is `True`, _dict_ collect\_dataframes(_packages=\[]_)[¶](broken-reference)

Collect dataframes of local data packages :param packages: List of packages to collect, defaults to all :type packages: listReturns

**(tuple)**Return type

Tuple of X(pandas.DataFrame), y(pandas.DataFrame) configure(_\*\*kwargs_)[¶](broken-reference)

Set Foundry config :keyword file: Path to the file containing :kwtype file: str :keyword (default: self.config.metadata\_file)

dataframe\_file (str): filename for the dataframe file default:”foundry\_dataframe.json” data\_file (str): : filename for the data file default:”foundry.hdf5” destination\_endpoint (str): Globus endpoint UUID where Foundry data should move local\_cache\_dir (str): Where to place collected data default:”./data”Returns

**(Foundry)**Return type

self: for chaining connect\_client_: Any_[¶](broken-reference) describe\_model()[¶](broken-reference) dlhub\_client_: Any_[¶](broken-reference) download(_globus=True_, _verbose=False_, _\*\*kwargs_)[¶](broken-reference)

Download a Foundry dataset :param globus: if True, use Globus to download the data else try HTTPS :type globus: bool :param verbose: if True print out debug information during the download :type verbose: boolReturns

**(Foundry)**Return type

self: for chaining forge\_client_: Any_[¶](broken-reference) get\_keys(_type_, _as\_object=False_)[¶](broken-reference)

Get keys for a Foundry datasetParameters

* **type** (_str_) – The type of key to be returned e.g., “input”, “target”
* **as\_object** (_bool_) – When `False`, will return a list of keys in as strings When `True`, will return the full key objects **Default:** `False`

Returns: (list) String representations of keys or if `as_object`

is False otherwise returns the full key objects. get\_packages(_paths=False_)[¶](broken-reference)

Get available local data packagesParameters

**paths** (_bool_) – If True return paths in addition to package, if False return package name onlyReturns

**(list)**Return type

List describing local Foundry packages list()[¶](broken-reference)

List available Foundry data packagesReturns

**(pandas.DataFrame)**Return type

DataFrame with summary list of Foundry data packages including name, title, and publication year load(_name_, _download=True_, _globus=True_, _verbose=False_, _metadata=None_, _\*\*kwargs_)[¶](broken-reference)

Load the metadata for a Foundry dataset into the client :param name: Name of the foundry dataset :type name: str :param download: If True, download the data associated with the package (default is True) :type download: bool :param globus: If True, download using Globus, otherwise https :type globus: bool :param verbose: If True print additional debug information :type verbose: bool :param metadata: **For debug purposes.** A search result analog to prepopulate metadata. :type metadata: dictKeyword Arguments

**interval** (_int_) – How often to poll Globus to check if transfers are completeReturnsReturn type

self load\_data(_source\_id=None_, _globus=True_)[¶](broken-reference)

Load in the data associated with the prescribed dataset

Tabular Data Type: Data are arranged in a standard data frame stored in self.dataframe\_file. The contents are read, and

File Data Type: <\<Add desc>>

For more complicated data structures, users should subclass Foundry and override the load\_data functionParameters

* **inputs** (_list_) – List of strings for input columns
* **targets** (_list_) – List of strings for output columns

Returns ——-s

> (tuple): Tuple of X, y values

&#x20;publish(_foundry\_metadata_, _data\_source_, _title_, _authors_, _update=False_, _publication\_year=None_, _\*\*kwargs_)[¶](broken-reference)

Submit a dataset for publication :param foundry\_metadata: Dict of metadata describing data package :type foundry\_metadata: dict :param data\_source: Url for Globus endpoint :type data\_source: string :param title: Title of data package :type title: string :param authors: List of data package author names e.g., Jack Black

> or Nunez, Victoria

Parameters

* **update** (_bool_) – True if this is an update to a prior data package (default: self.config.metadata\_file)
* **publication\_year** (_int_) – Year of dataset publication. If None, will be set to the current calendar year by MDF Connect Client. (default: $current\_year)

Keyword Arguments

* **affiliations** ([_list_](broken-reference)) – List of author affiliations
* **tags** ([_list_](broken-reference)) – List of tags to apply to the data package
* **short\_name** (_string_) – Shortened/abbreviated name of the data package
* **publisher** (_string_) – Data publishing entity (e.g. MDF, Zenodo, etc.)

Returns

**(dict) MDF Connect Response** – of dataset. Contains source\_id, which can be used to check the status of the submissionReturn type

Response from MDF Connect to allow tracking publish\_model(_options_)[¶](broken-reference)

Submit a model or function for publication :param options: dict of all possible optionsOptions keys:

title (req) authors (req) short\_name (req) servable\_type (req) (“static method”, “class method”, “keras”, “pytorch”, “tensorflow”, “sklearn”) affiliations domains abstract references requirements (dict of library:version keypairs) module (if Python method) function (if Python method) inputs (not needed for TF) (dict of options) outputs (not needed for TF) methods (e.g. research methods) DOI publication\_year (advanced) version (advanced) visibility (dict of users and groups, each a list) funding reference rights

TODO: alternate identifier (to add an identifier of this artifact in another service) add file add directory add files run(_name_, _inputs_, _\*\*kwargs_)[¶](broken-reference)

Run a model on dataParameters

* **name** (_str_) – DLHub model name
* **inputs** – Data to send to DLHub as inputs (should be JSON serializable)

ReturnsReturn type

Returns results after invocation via the DLHub service

* Pass [\*\*](broken-reference)kwargs through to DLHub client and document kwargs

&#x20;xtract\_tokens_: Any_[¶](broken-reference)

## foundry.models module[¶](broken-reference)

&#x20;_class_ foundry.models.FoundryConfig(_\*_, _dataframe\_file: str = 'foundry\_dataframe.json'_, _data\_file: str = 'foundry.hdf5'_, _metadata\_file: str = 'foundry\_metadata.json'_, _destination\_endpoint: str = None_, _local: bool = False_, _metadata\_key: str = 'foundry'_, _organization: str = 'foundry'_, _local\_cache\_dir: str = './data'_)[¶](broken-reference)

Bases: `pydantic.main.BaseModel`

Foundry Configuration Configuration information for Foundry DatasetParameters

* **dataframe\_file** (_str_) – Filename to read dataframe contents from
* **metadata\_file** (_str_) – Filename to read metadata contents from defaults to reading for MDF Discover
* **destination\_endpoint** (_str_) – Globus endpoint ID to transfer data to (defaults to local GCP installation)
* **local\_cache\_dir** (_str_) – Path to local Foundry package cache

&#x20;data\_file_: Optional\[str]_[¶](broken-reference) dataframe\_file_: Optional\[str]_[¶](broken-reference) destination\_endpoint_: Optional\[str]_[¶](broken-reference) local_: Optional\[bool]_[¶](broken-reference) metadata\_file_: Optional\[str]_[¶](broken-reference) metadata\_key_: Optional\[str]_[¶](broken-reference) organization_: Optional\[str]_[¶](broken-reference) _class_ foundry.models.FoundryDataset(_\*_, _keys: List\[_[_foundry.models.FoundryKey_](broken-reference)_] = None_, _splits: List\[_[_foundry.models.FoundrySplit_](broken-reference)_] = None_, _type:_ [_foundry.models.FoundryDatasetType_](broken-reference) _= None_, _short\_name: str = ''_, _dataframe: Any = None_)[¶](broken-reference)

Bases: `pydantic.main.BaseModel`

Foundry Dataset Schema for Foundry Datasets. This includes specifications of inputs, outputs, type, version, and more _class_ Config[¶](broken-reference)

Bases: `object` arbitrary\_types\_allowed _= True_[¶](broken-reference) dataframe_: Optional\[Any]_[¶](broken-reference) keys_: List\[_[_foundry.models.FoundryKey_](broken-reference)_]_[¶](broken-reference) short\_name_: Optional\[str]_[¶](broken-reference) splits_: Optional\[List\[_[_foundry.models.FoundrySplit_](broken-reference)_]]_[¶](broken-reference) type_:_ [_foundry.models.FoundryDatasetType_](broken-reference)[¶](broken-reference) _class_ foundry.models.FoundryDatasetType(_value_)[¶](broken-reference)

Bases: `enum.Enum`

Foundry Dataset Types Enumeration of the possible Foundry dataset types files _= 'files'_[¶](broken-reference) hdf5 _= 'hdf5'_[¶](broken-reference) other _= 'other'_[¶](broken-reference) tabular _= 'tabular'_[¶](broken-reference) _class_ foundry.models.FoundryKey(_\*_, _key: List\[str] = \[]_, _type: str = ''_, _filter: str = ''_, _units: str = ''_, _description: str = ''_, _classes: List\[_[_foundry.models.FoundryKeyClass_](broken-reference)_] = None_)[¶](broken-reference)

Bases: `pydantic.main.BaseModel` classes_: Optional\[List\[_[_foundry.models.FoundryKeyClass_](broken-reference)_]]_[¶](broken-reference) description_: Optional\[str]_[¶](broken-reference) filter_: Optional\[str]_[¶](broken-reference) key_: List\[str]_[¶](broken-reference) type_: str_[¶](broken-reference) units_: Optional\[str]_[¶](broken-reference) _class_ foundry.models.FoundryKeyClass(_\*_, _label: str = ''_, _name: str = ''_)[¶](broken-reference)

Bases: `pydantic.main.BaseModel` label_: str_[¶](broken-reference) name_: str_[¶](broken-reference) _class_ foundry.models.FoundryMetadata(_\*_, _dc: Dict = {}_, _mdf: Dict = {}_, _dataset:_ [_foundry.models.FoundryDataset_](broken-reference) _= {}_, _config:_ [_foundry.models.FoundryConfig_](broken-reference) _= FoundryConfig(dataframe\_file='foundry\_dataframe.json', data\_file='foundry.hdf5', metadata\_file='foundry\_metadata.json', destination\_endpoint=None, local=False, metadata\_key='foundry', organization='foundry', local\_cache\_dir='./data')_)[¶](broken-reference)

Bases: `pydantic.main.BaseModel` _class_ Config[¶](broken-reference)

Bases: `object` arbitrary\_types\_allowed _= True_[¶](broken-reference) config_:_ [_foundry.models.FoundryConfig_](broken-reference)[¶](broken-reference) dataset_:_ [_foundry.models.FoundryDataset_](broken-reference)[¶](broken-reference) dc_: Optional\[Dict]_[¶](broken-reference) mdf_: Optional\[Dict]_[¶](broken-reference) _class_ foundry.models.FoundrySpecification(_\*_, _name: str = ''_, _version: str = ''_, _description: str = ''_, _private: bool = False_, _dependencies: Any = None_)[¶](broken-reference)

Bases: `pydantic.main.BaseModel`

Pydantic base class for interacting with the Foundry data package specification The specification provides a way to group datasets and manage versions add\_dependency(_name_, _version_)[¶](broken-reference) clear\_dependencies()[¶](broken-reference) dependencies_: Any_[¶](broken-reference) description_: str_[¶](broken-reference) name_: str_[¶](broken-reference) private_: bool_[¶](broken-reference) remove\_duplicate\_dependencies()[¶](broken-reference) version_: str_[¶](broken-reference) _class_ foundry.models.FoundrySpecificationDataset(_\*_, _name: str = None_, _provider: str = 'MDF'_, _version: str = None_)[¶](broken-reference)

Bases: `pydantic.main.BaseModel`

Pydantic base class for datasets within the Foundry data package specification name_: Optional\[str]_[¶](broken-reference) provider_: Optional\[str]_[¶](broken-reference) version_: Optional\[str]_[¶](broken-reference) _class_ foundry.models.FoundrySplit(_\*_, _type: str = ''_, _path: str = ''_, _label: str = ''_)[¶](broken-reference)

Bases: `pydantic.main.BaseModel` label_: Optional\[str]_[¶](broken-reference) path_: Optional\[str]_[¶](broken-reference) type_: str_[¶](broken-reference)

## foundry.xtract\_method module[¶](broken-reference)
