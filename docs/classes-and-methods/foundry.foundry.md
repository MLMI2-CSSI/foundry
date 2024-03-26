# foundry.foundry

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L0)

## module `foundry.foundry`

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L30)

### class `HiddenColumnDataFrame`

A subclass of pd.DataFrame that supports hiding a specific column. This is intended to mimic display of search results from an earlier version while providing access to associated FoundryDataset objects for each entry in the dataframe via the `get_dataset_by_[name/doi]()` function.

**Parameters:** \*args: positional arguments Positional arguments passed to the parent class constructor. hidden\_column: str, optional The name of the column to be hidden. \*\*kwargs: keyword arguments Keyword arguments passed to the parent class constructor.

**Attributes:** hidden\_column: str or None The name of the hidden column.

Methods: _repr\_html_(): Overrides the _repr\_html_ method of the parent class to hide the specified column in the HTML representation. get\_dataset\_by\_name(dataset\_name): Returns the FoundryDataset associated with the given dataset name. Can also handle a DOI. get\_dataset\_by\_doi(doi): Returns the FoundryDataset associated with the given DOI.

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L59)

#### method `__init__`

```python
__init__(*args, hidden_column=None, **kwargs)
```

***

**property T**

The transpose of the DataFrame.

Returns ------- DataFrame The transposed DataFrame.

See Also -------- DataFrame.transpose : Transpose index and columns.

Examples -------- `df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})` `df` col1 col2 0 1 3 1 2 4

`df.T` 0 1 col1 1 2 col2 3 4

***

**property at**

Access a single value for a row/column label pair.

Similar to `loc`, in that both provide label-based lookups. Use `at` if you only need to get or set a single value in a DataFrame or Series.

Raises ------ KeyError If getting a value and 'label' does not exist in a DataFrame or Series.

ValueError If row/column label pair is not a tuple or if any label from the pair is not a scalar for DataFrame. If label is list-like (_excluding_ NamedTuple) for Series.

See Also -------- DataFrame.at : Access a single value for a row/column pair by label. DataFrame.iat : Access a single value for a row/column pair by integer position. DataFrame.loc : Access a group of rows and columns by label(s). DataFrame.iloc : Access a group of rows and columns by integer position(s). Series.at : Access a single value by label. Series.iat : Access a single value by integer position. Series.loc : Access a group of rows by label(s). Series.iloc : Access a group of rows by integer position(s).

Notes ----- See :ref:`Fast scalar value getting and setting <indexing.basics.get_value>` for more details.

Examples -------- `df = pd.DataFrame([[0, 2, 3], [0, 4, 1], [10, 20, 30]],` ... index=\[4, 5, 6], columns=\['A', 'B', 'C']) `df` A B C 4 0 2 3 5 0 4 1 6 10 20 30

Get value at specified row/column pair

`df.at[4, 'B']` 2

Set value at specified row/column pair

`df.at[4, 'B'] = 10` `df.at[4, 'B']` 10

Get value within a Series

`df.loc[5].at['B']` 4

***

**property attrs**

Dictionary of global attributes of this dataset.

.. warning:

```

    attrs is experimental and may change without warning. 

```

See Also -------- DataFrame.flags : Global flags applying to this object.

Notes ----- Many operations that create new datasets will copy `attrs`. Copies are always deep so that changing `attrs` will only affect the present dataset. `pandas.concat` copies `attrs` only if all input datasets have the same `attrs`.

Examples -------- For Series:

`ser = pd.Series([1, 2, 3])` `ser.attrs = {"A": [10, 20, 30]}` `ser.attrs` {'A': \[10, 20, 30]}

For DataFrame:

`df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})` `df.attrs = {"A": [10, 20, 30]}` `df.attrs` {'A': \[10, 20, 30]}

***

**property axes**

Return a list representing the axes of the DataFrame.

It has the row axis labels and column axis labels as the only members. They are returned in that order.

Examples -------- `df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})` `df.axes` \[RangeIndex(start=0, stop=2, step=1), Index(\['col1', 'col2'], dtype='object')]

***

**property dtypes**

Return the dtypes in the DataFrame.

This returns a Series with the data type of each column. The result's index is the original DataFrame's columns. Columns with mixed types are stored with the `object` dtype. See :ref:`the User Guide <basics.dtypes>` for more.

Returns ------- pandas.Series The data type of each column.

Examples -------- `df = pd.DataFrame({'float': [1.0],` ... 'int': \[1], ... 'datetime': \[pd.Timestamp('20180310')], ... 'string': \['foo']}) `df.dtypes` float float64 int int64 datetime datetime64\[ns] string object dtype: object

***

**property empty**

Indicator whether Series/DataFrame is empty.

True if Series/DataFrame is entirely empty (no items), meaning any of the axes are of length 0.

Returns ------- bool If Series/DataFrame is empty, return True, if not return False.

See Also -------- Series.dropna : Return series without null values. DataFrame.dropna : Return DataFrame with labels on given axis omitted where (all or any) data are missing.

Notes ----- If Series/DataFrame contains only NaNs, it is still not considered empty. See the example below.

Examples -------- An example of an actual empty DataFrame. Notice the index is empty:

`df_empty = pd.DataFrame({'A' : []})` `df_empty` Empty DataFrame Columns: \[A] Index: \[] `df_empty.empty` True

If we only have NaNs in our DataFrame, it is not considered empty! We will need to drop the NaNs to make the DataFrame empty:

`df = pd.DataFrame({'A' : [np.nan]})` `df` A 0 NaN `df.empty` False `df.dropna().empty` True

`ser_empty = pd.Series({'A' : []})` `ser_empty` A \[] dtype: object `ser_empty.empty` False `ser_empty = pd.Series()` `ser_empty.empty` True

***

**property flags**

Get the properties associated with this pandas object.

The available flags are

* :attr:`Flags.allows_duplicate_labels`

See Also -------- Flags : Flags that apply to pandas objects. DataFrame.attrs : Global metadata applying to this dataset.

Notes ----- "Flags" differ from "metadata". Flags reflect properties of the pandas object (the Series or DataFrame). Metadata refer to properties of the dataset, and should be stored in :attr:`DataFrame.attrs`.

Examples -------- `df = pd.DataFrame({"A": [1, 2]})` `df.flags` \<Flags(allows\_duplicate\_labels=True)>

Flags can be get or set using `.`

`df.flags.allows_duplicate_labels` True `df.flags.allows_duplicate_labels = False`

Or by slicing with a key

`df.flags["allows_duplicate_labels"]` False `df.flags["allows_duplicate_labels"] = True`

***

**property iat**

Access a single value for a row/column pair by integer position.

Similar to `iloc`, in that both provide integer-based lookups. Use `iat` if you only need to get or set a single value in a DataFrame or Series.

Raises ------ IndexError When integer position is out of bounds.

See Also -------- DataFrame.at : Access a single value for a row/column label pair. DataFrame.loc : Access a group of rows and columns by label(s). DataFrame.iloc : Access a group of rows and columns by integer position(s).

Examples -------- `df = pd.DataFrame([[0, 2, 3], [0, 4, 1], [10, 20, 30]],` ... columns=\['A', 'B', 'C']) `df` A B C 0 0 2 3 1 0 4 1 2 10 20 30

Get value at specified row/column pair

`df.iat[1, 2]` 1

Set value at specified row/column pair

`df.iat[1, 2] = 10` `df.iat[1, 2]` 10

Get value within a series

`df.loc[0].iat[1]` 2

***

**property iloc**

Purely integer-location based indexing for selection by position.

.. deprecated:: 2.2.0

Returning a tuple from a callable is deprecated.

`.iloc[]` is primarily integer position based (from `0` to `length-1` of the axis), but may also be used with a boolean array.

Allowed inputs are:

* An integer, e.g. `5`.
* A list or array of integers, e.g. `[4, 3, 0]`.
* A slice object with ints, e.g. `1:7`.
* A boolean array.
* A `callable` function with one argument (the calling Series or DataFrame) and that returns valid output for indexing (one of the above). This is useful in method chains, when you don't have a reference to the calling object, but would like to base your selection on some value.
* A tuple of row and column indexes. The tuple elements consist of one of the above inputs, e.g. `(0, 1)`.

`.iloc` will raise `IndexError` if a requested indexer is out-of-bounds, except _slice_ indexers which allow out-of-bounds indexing (this conforms with python/numpy _slice_ semantics).

See more at :ref:`Selection by Position <indexing.integer>`.

See Also -------- DataFrame.iat : Fast integer location scalar accessor. DataFrame.loc : Purely label-location based indexer for selection by label. Series.iloc : Purely integer-location based indexing for selection by position.

Examples -------- `mydict = [{'a': 1, 'b': 2, 'c': 3, 'd': 4},` ... {'a': 100, 'b': 200, 'c': 300, 'd': 400}, ... {'a': 1000, 'b': 2000, 'c': 3000, 'd': 4000}] `df = pd.DataFrame(mydict)` `df` a b c d 0 1 2 3 4 1 100 200 300 400 2 1000 2000 3000 4000

**Indexing just the rows**

With a scalar integer.

`type(df.iloc[0])` \<class 'pandas.core.series.Series'> `df.iloc[0]` a 1 b 2 c 3 d 4 Name: 0, dtype: int64

With a list of integers.

`df.iloc[[0]]` a b c d 0 1 2 3 4 `type(df.iloc[[0]])` \<class 'pandas.core.frame.DataFrame'>

`df.iloc[[0, 1]]` a b c d 0 1 2 3 4 1 100 200 300 400

With a `slice` object.

`df.iloc[:3]` a b c d 0 1 2 3 4 1 100 200 300 400 2 1000 2000 3000 4000

With a boolean mask the same length as the index.

`df.iloc[[True, False, True]]` a b c d 0 1 2 3 4 2 1000 2000 3000 4000

With a callable, useful in method chains. The `x` passed to the `lambda` is the DataFrame being sliced. This selects the rows whose index label even.

`df.iloc[lambda x: x.index % 2 == 0]` a b c d 0 1 2 3 4 2 1000 2000 3000 4000

**Indexing both axes**

You can mix the indexer types for the index and columns. Use `:` to select the entire axis.

With scalar integers.

`df.iloc[0, 1]` 2

With lists of integers.

`df.iloc[[0, 2], [1, 3]]` b d 0 2 4 2 2000 4000

With `slice` objects.

`df.iloc[1:3, 0:3]` a b c 1 100 200 300 2 1000 2000 3000

With a boolean array whose length matches the columns.

`df.iloc[:, [True, False, True, False]]` a c 0 1 3 1 100 300 2 1000 3000

With a callable function that expects the Series or DataFrame.

`df.iloc[:, lambda df: [0, 2]]` a c 0 1 3 1 100 300 2 1000 3000

***

**property loc**

Access a group of rows and columns by label(s) or a boolean array.

`.loc[]` is primarily label based, but may also be used with a boolean array.

Allowed inputs are:

* A single label, e.g. `5` or `'a'`, (note that `5` is interpreted as a _label_ of the index, and **never** as an integer position along the index).
* A list or array of labels, e.g. `['a', 'b', 'c']`.
* A slice object with labels, e.g. `'a':'f'`.

.. warning:: Note that contrary to usual python slices, **both** the start and the stop are included

* A boolean array of the same length as the axis being sliced, e.g. `[True, False, True]`.
* An alignable boolean Series. The index of the key will be aligned before masking.
* An alignable Index. The Index of the returned selection will be the input.
* A `callable` function with one argument (the calling Series or DataFrame) and that returns valid output for indexing (one of the above)

See more at :ref:`Selection by Label <indexing.label>`.

Raises ------ KeyError If any items are not found. IndexingError If an indexed key is passed and its index is unalignable to the frame index.

See Also -------- DataFrame.at : Access a single value for a row/column label pair. DataFrame.iloc : Access group of rows and columns by integer position(s). DataFrame.xs : Returns a cross-section (row(s) or column(s)) from the Series/DataFrame. Series.loc : Access group of values using labels.

Examples -------- **Getting values**

`df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],` ... index=\['cobra', 'viper', 'sidewinder'], ... columns=\['max\_speed', 'shield']) `df` max\_speed shield cobra 1 2 viper 4 5 sidewinder 7 8

Single label. Note this returns the row as a Series.

`df.loc['viper']` max\_speed 4 shield 5 Name: viper, dtype: int64

List of labels. Note using `[[]]` returns a DataFrame.

`df.loc[['viper', 'sidewinder']]` max\_speed shield viper 4 5 sidewinder 7 8

Single label for row and column

`df.loc['cobra', 'shield']` 2

Slice with labels for row and single label for column. As mentioned above, note that both the start and stop of the slice are included.

`df.loc['cobra':'viper', 'max_speed']` cobra 1 viper 4 Name: max\_speed, dtype: int64

Boolean list with the same length as the row axis

`df.loc[[False, False, True]]` max\_speed shield sidewinder 7 8

Alignable boolean Series:

`df.loc[pd.Series([False, True, False],` ... index=\['viper', 'sidewinder', 'cobra'])] max\_speed shield sidewinder 7 8

Index (same behavior as `df.reindex`)

`df.loc[pd.Index(["cobra", "viper"], name="foo")]` max\_speed shield foo cobra 1 2 viper 4 5

Conditional that returns a boolean Series

`df.loc[df['shield'] > 6]` max\_speed shield sidewinder 7 8

Conditional that returns a boolean Series with column labels specified

`df.loc[df['shield'] > 6, ['max_speed']]` max\_speed sidewinder 7

Multiple conditional using `&` that returns a boolean Series

`df.loc[(df['max_speed'] > 1) & (df['shield'] < 8)]` max\_speed shield viper 4 5

Multiple conditional using `|` that returns a boolean Series

`df.loc[(df['max_speed'] > 4) | (df['shield'] < 5)]` max\_speed shield cobra 1 2 sidewinder 7 8

Please ensure that each condition is wrapped in parentheses `()`. See the :ref:`user guide<indexing.boolean>` for more details and explanations of Boolean indexing.

.. note:

```
     If you find yourself using 3 or more conditionals in ``.loc[]``,
     consider using :ref:`advanced indexing<advanced.advanced_hierarchical>`.

     See below for using ``.loc[]`` on MultiIndex DataFrames.

```

Callable that returns a boolean Series

`df.loc[lambda df: df['shield'] == 8]` max\_speed shield sidewinder 7 8

**Setting values**

Set value for all items matching the list of labels

`df.loc[['viper', 'sidewinder'], ['shield']] = 50` `df` max\_speed shield cobra 1 2 viper 4 50 sidewinder 7 50

Set value for an entire row

`df.loc['cobra'] = 10` `df` max\_speed shield cobra 10 10 viper 4 50 sidewinder 7 50

Set value for an entire column

`df.loc[:, 'max_speed'] = 30` `df` max\_speed shield cobra 30 10 viper 30 50 sidewinder 30 50

Set value for rows matching callable condition

`df.loc[df['shield'] > 35] = 0` `df` max\_speed shield cobra 30 10 viper 0 0 sidewinder 0 0

Add value matching location

`df.loc["viper", "shield"] += 5` `df` max\_speed shield cobra 30 10 viper 0 5 sidewinder 0 0

Setting using a `Series` or a `DataFrame` sets the values matching the index labels, not the index positions.

`shuffled_df = df.loc[["viper", "cobra", "sidewinder"]]` `df.loc[:] += shuffled_df` `df` max\_speed shield cobra 60 20 viper 0 10 sidewinder 0 0

**Getting values on a DataFrame with an index that has integer labels**

Another example using integers for the index

`df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],` ... index=\[7, 8, 9], columns=\['max\_speed', 'shield']) `df` max\_speed shield 7 1 2 8 4 5 9 7 8

Slice with integer labels for rows. As mentioned above, note that both the start and stop of the slice are included.

`df.loc[7:9]` max\_speed shield 7 1 2 8 4 5 9 7 8

**Getting values with a MultiIndex**

A number of examples using a DataFrame with a MultiIndex

`tuples = [` ... ('cobra', 'mark i'), ('cobra', 'mark ii'), ... ('sidewinder', 'mark i'), ('sidewinder', 'mark ii'), ... ('viper', 'mark ii'), ('viper', 'mark iii') ... ] `index = pd.MultiIndex.from_tuples(tuples)` `values = [[12, 2], [0, 4], [10, 20],` ... \[1, 4], \[7, 1], \[16, 36]] `df = pd.DataFrame(values, columns=['max_speed', 'shield'], index=index)` `df` max\_speed shield cobra mark i 12 2 mark ii 0 4 sidewinder mark i 10 20 mark ii 1 4 viper mark ii 7 1 mark iii 16 36

Single label. Note this returns a DataFrame with a single index.

`df.loc['cobra']` max\_speed shield mark i 12 2 mark ii 0 4

Single index tuple. Note this returns a Series.

`df.loc[('cobra', 'mark ii')]` max\_speed 0 shield 4 Name: (cobra, mark ii), dtype: int64

Single label for row and column. Similar to passing in a tuple, this returns a Series.

`df.loc['cobra', 'mark i']` max\_speed 12 shield 2 Name: (cobra, mark i), dtype: int64

Single tuple. Note using `[[]]` returns a DataFrame.

`df.loc[[('cobra', 'mark ii')]]` max\_speed shield cobra mark ii 0 4

Single tuple for the index with a single label for the column

`df.loc[('cobra', 'mark i'), 'shield']` 2

Slice from index tuple to single label

`df.loc[('cobra', 'mark i'):'viper']` max\_speed shield cobra mark i 12 2 mark ii 0 4 sidewinder mark i 10 20 mark ii 1 4 viper mark ii 7 1 mark iii 16 36

Slice from index tuple to index tuple

`df.loc[('cobra', 'mark i'):('viper', 'mark ii')]` max\_speed shield cobra mark i 12 2 mark ii 0 4 sidewinder mark i 10 20 mark ii 1 4 viper mark ii 7 1

Please see the :ref:`user guide<advanced.advanced_hierarchical>` for more details and explanations of advanced indexing.

***

**property ndim**

Return an int representing the number of axes / array dimensions.

Return 1 if Series. Otherwise return 2 if DataFrame.

See Also -------- ndarray.ndim : Number of array dimensions.

Examples -------- `s = pd.Series({'a': 1, 'b': 2, 'c': 3})` `s.ndim` 1

`df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})` `df.ndim` 2

***

**property shape**

Return a tuple representing the dimensionality of the DataFrame.

See Also -------- ndarray.shape : Tuple of array dimensions.

Examples -------- `df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})` `df.shape` (2, 2)

`df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4],` ... 'col3': \[5, 6]}) `df.shape` (2, 3)

***

**property size**

Return an int representing the number of elements in this object.

Return the number of rows if Series. Otherwise return the number of rows times number of columns if DataFrame.

See Also -------- ndarray.size : Number of elements in the array.

Examples -------- `s = pd.Series({'a': 1, 'b': 2, 'c': 3})` `s.size` 3

`df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})` `df.size` 4

***

**property style**

Returns a Styler object.

Contains methods for building a styled HTML representation of the DataFrame.

See Also -------- io.formats.style.Styler : Helps style a DataFrame or Series according to the data with HTML and CSS.

Examples -------- `df = pd.DataFrame({'A': [1, 2, 3]})` `df.style # doctest: +SKIP`

Please see `Table Visualization <../../user_guide/style.ipynb>`\_ for more examples.

***

**property values**

Return a Numpy representation of the DataFrame.

.. warning:

```

    We recommend using :meth:`DataFrame.to_numpy` instead. 

```

Only the values in the DataFrame will be returned, the axes labels will be removed.

Returns ------- numpy.ndarray The values of the DataFrame.

See Also -------- DataFrame.to\_numpy : Recommended alternative to this method. DataFrame.index : Retrieve the index labels. DataFrame.columns : Retrieving the column names.

Notes ----- The dtype will be a lower-common-denominator dtype (implicit upcasting); that is to say if the dtypes (even of numeric types) are mixed, the one that accommodates all will be chosen. Use this with care if you are not dealing with the blocks.

e.g. If the dtypes are float16 and float32, dtype will be upcast to float32. If dtypes are int32 and uint8, dtype will be upcast to int32. By :func:`numpy.find_common_type` convention, mixing int64 and uint64 will result in a float64 dtype.

Examples -------- A DataFrame where all columns are the same type (e.g., int64) results in an array of the same type.

`df = pd.DataFrame({'age': [ 3, 29],` ... 'height': \[94, 170], ... 'weight': \[31, 115]}) `df` age height weight 0 3 94 31 1 29 170 115 `df.dtypes` age int64 height int64 weight int64 dtype: object `df.values` array(\[\[ 3, 94, 31], \[ 29, 170, 115]])

A DataFrame with mixed type columns(e.g., str/object, int64, float32) results in an ndarray of the broadest type that accommodates these mixed types (e.g., object).

`df2 = pd.DataFrame([('parrot', 24.0, 'second'),` ... ('lion', 80.5, 1), ... ('monkey', np.nan, None)], ... columns=('name', 'max\_speed', 'rank')) `df2.dtypes` name object max\_speed float64 rank object dtype: object `df2.values` array(\[\['parrot', 24.0, 'second'], \['lion', 80.5, 1], \['monkey', nan, None]], dtype=object)

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L73)

#### method `get_dataset_by_doi`

```python
get_dataset_by_doi(doi)
```

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L67)

#### method `get_dataset_by_name`

```python
get_dataset_by_name(dataset_name)
```

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L77)

### class `Foundry`

Foundry Client Base Class

This class represents a client for interacting with the Foundry service. It provides methods for searching and accessing datasets, as well as publishing new datasets.

**Attributes:**

* `dlhub_client` (Any): The DLHub client.
* `forge_client` (Any): The Forge client.
* `connect_client` (Any): The MDF Connect client.
* `transfer_client` (Any): The Globus transfer client.
* `auth_client` (Any): The authentication client.
* `index` (str): The index to use for search and data publication.
* `auths` (Any): The authorizers used for authentication.

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L102)

#### method `__init__`

```python
__init__(
    no_browser: bool = False,
    no_local_server: bool = False,
    index: str = 'mdf',
    authorizers: dict = None,
    use_globus: bool = True,
    verbose: bool = False,
    interval: int = 10,
    local_cache_dir: str = None,
    **data
)
```

Initialize a Foundry client

**Args:**

* `no_browser` (bool): Whether to open the browser for the Globus Auth URL.
* `no_local_server` (bool): Whether a local server is available. This should be `False` when on a remote server (e.g., Google Colab).
* `index` (str): Index to use for search and data publication. Choices are `mdf` or `mdf-test`.
* `authorizers` (dict): A dictionary of authorizers to use, following the `mdf_toolbox` format.
* `use_globus` (bool): If True, download using Globus, otherwise use HTTPS.
* `verbose` (bool): If True, print additional debug information.
* `interval` (int): How often to poll Globus to check if transfers are complete.
* `local_cache_dir` (str): Optional location to store downloaded data. If not specified, defaults to either environmental variable ('FOUNDRY\_LOCAL\_CACHE\_DIR') or './data'
* `data` (dict): Other arguments, e.g., results from an MDF search result that are used to populate Foundry metadata fields.

**Returns:** An initialized and authenticated Foundry client.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L501)

#### method `check_status`

```python
check_status(source_id, short=False, raw=False)
```

Check the status of your submission.

**Arguments:**

* `source_id` (str): The `source_id` (`source_name` + version information) of the submission to check. Returned in the `res` result from `publish()` via MDF Connect Client.
* `short` (bool): When `False`, will print a status summary containing all of the status steps for the dataset. When `True`, will print a short finished/processing message, useful for checking many datasets' status at once.
* `**Default`: \*\* `False`
* `raw` (bool): When `False`, will print a nicely-formatted status summary. When `True`, will return the full status result. For direct human consumption, `False` is recommended.
* `**Default`: \*\* `False`

**Returns:**

* `If ``raw`` is ``True``, *dict*`: The full status result.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L268)

#### method `dataset_from_metadata`

```python
dataset_from_metadata(metadata: dict) → FoundryDataset
```

Converts the result of a forge query to a FoundryDatset object

**Args:**

* `metadata` (dict): result from a forge query

**Returns:**

* `FoundryDataset`: a FoundryDataset object created from the metadata

**Raises:**

* `Exception`: If the mdf entry is missing a section, cannot generate a foundry dataset object

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L341)

#### method `filter_datasets_by_query`

```python
filter_datasets_by_query(query_string: str, metadata: List[Dict]) → List[Dict]
```

Filters the given metadata based on the provided query string.

**Args:**

* `query_string` (str): The query string to filter the metadata.
* `metadata` (list): The list of metadata to be filtered.

**Returns:**

* `list[dict]`: A list of dicts that match the query string.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L300)

#### method `get_metadata_by_doi`

```python
get_metadata_by_doi(doi: str) → dict
```

Query foundry datasets by DOI

Should only return a single result.

**Args:**

* `doi` (str): doi of desired dataset

**Returns:**

* `metadata` (dict): result from a forge query

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L319)

#### method `get_metadata_by_query`

```python
get_metadata_by_query(q: str, limit: int) → dict
```

Submit query to forge client and return results

**Args:**

* `q` (str): query string The query string to be submitted to the forge client.
* `limit` (int): maximum number of results to return The maximum number of results to be returned by the foundry client.

**Returns:**

* `metadata` (dict): result from a forge query The result from the forge query, represented as a dictionary.

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L257)

#### method `list`

```python
list(limit: int = None)
```

List available Foundry datasets

**Args:**

* `limit` (int): maximum number of results to return

**Returns:**

* `List[FoundryDataset]`: List of FoundryDataset objects

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L378)

#### method `publish_dataset`

```python
publish_dataset(
    foundry_metadata: Dict[str, Any],
    title: str,
    authors: List[str],
    https_data_path: str = None,
    globus_data_source: str = None,
    update: bool = False,
    publication_year: int = None,
    test: bool = False,
    **kwargs: Dict[str, Any]
) → Dict[str, Any]
```

Submit a dataset for publication; can choose to submit via HTTPS using `https_data_path` or via Globus Transfer using the `globus_data_source` argument. Only one upload method may be specified.

**Args:**

* `foundry_metadata` (dict): Dict of metadata describing data package
* `title` (string): Title of data package
* `authors` (list): List of data package author names e.g., Jack Black or Nunez, Victoria
* `https_data_path` (str): Path to the local dataset to publish to Foundry via HTTPS. Creates an HTTPS PUT request to upload the data specified to a Globus endpoint (default is NCSA endpoint) before it is transferred to MDF. If None, the user must specify a 'globus\_data\_source' URL to the location of the data on their own Globus endpoint. User must choose either `globus_data_source` or `https_data_path` to publish their data.
* `globus_data_source` (str): Url path for a data folder on a Globus endpoint; url can be obtained through the Globus Web UI or SDK. If None, the user must specify an 'https\_data\_path' pointing to the location of the data on their local machine. User must choose either `globus_data_source` or `https_data_path` to publish their data.
* `update` (bool): True if this is an update to a prior data package
* `(default`: self.config.metadata\_file)
* `publication_year` (int): Year of dataset publication. If None, will be set to the current calendar year by MDF Connect Client.
* `(default`: $current\_year)
* `test` (bool): If True, do not submit the dataset for publication (ie transfer to the MDF endpoint). Default is False.

Keyword Args:

* `affiliations` (list): List of author affiliations
* `tags` (list): List of tags to apply to the data package
* `short_name` (string): Shortened/abbreviated name of the data package
* `publisher` (string): Data publishing entity (e.g. MDF, Zenodo, etc.)
* `description` (str): A description of the dataset.
* `dataset_doi` (str): The DOI for this dataset (not an associated paper).
* `related_dois` (list): DOIs related to this dataset, not including the dataset's own DOI (for example, an associated paper's DOI).

Returns ------- (dict) MDF Connect Response: Response from MDF Connect to allow tracking of dataset. Contains `source_id`, which can be used to check the status of the submission

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L475)

#### method `publish_model`

```python
publish_model(
    title,
    creators,
    short_name,
    servable_type,
    serv_options,
    affiliations=None,
    paper_doi=None
)
```

Simplified publishing method for servables

**Args:**

* `title` (string): title for the servable
* `creators` (string | list): either the creator's name (FamilyName, GivenName) or a list of the creators' names
* `short_name` (string): shorthand name for the servable
* `servable_type` (string): the type of the servable, must be a member of ("static\_method", "class\_method", "keras", "pytorch", "tensorflow", "sklearn")
* `serv_options` (dict): the servable\_type specific arguments that are necessary for publishing. arguments can be found at
* `https`: //dlhub-sdk.readthedocs.io/en/latest/source/dlhub\_sdk.models.servables.html under the appropriate `create_model` signature. use the argument names as keys and their values as the values.
* `affiliations` (list): list of affiliations for each author
* `paper_doi` (str): DOI of a paper that describes the servable

**Returns:**

* `(string)`: task id of this submission, can be used to check for success

**Raises:**

* `ValueError`: If the given servable\_type is not in the list of acceptable types
* `Exception`: If the serv\_options are incomplete or the request to publish results in an error

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L209)

#### method `search`

```python
search(
    query: str = None,
    limit: int = None,
    as_list: bool = False
) → [<class 'FoundryDataset'>]
```

Search available Foundry datasets

This method searches for available Foundry datasets based on the provided query string. If a DOI is provided as the query, it retrieves the metadata for that specific dataset. If a query string is provided, it retrieves the metadata for datasets that match the query. The limit parameter can be used to specify the maximum number of results to return.

**Args:**

* `query` (str): The query string to match. If a DOI is provided, it retrieves the metadata for that specific dataset.
* `limit` (int): The maximum number of results to return.
* `as_list` (bool): If True, the search results will be returned as a list instead of a DataFrame.

**Returns:**

* `List[FoundryDataset] or DataFrame`: A list of search results as FoundryDataset objects or a DataFrame if as\_list is False.

**Raises:**

* `Exception`: If no results are found for the provided query.

**Example:** `foundry = Foundry()` >>> results = foundry.search(query="materials science", limit=10) >>> print(len(results)) 10

***

[![](https://img.shields.io/badge/-source-cccccc?style=flat-square)](https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L358)

#### method `search_results_to_dataframe`

```python
search_results_to_dataframe(results)
```

Convert a list of results into a pandas DataFrame.

**Args:**

* `results` (list): A list of results.

**Returns:**

* `DataFrame`: A pandas DataFrame containing the converted results.

***

_This file was automatically generated via_ [_lazydocs_](https://github.com/ml-tooling/lazydocs)_._
