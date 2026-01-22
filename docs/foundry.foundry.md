<!-- markdownlint-disable -->

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `foundry.foundry`






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `HiddenColumnDataFrame`
A subclass of pd.DataFrame that supports hiding a specific column. This is intended to mimic display of search results from an earlier version while providing access to associated FoundryDataset objects for each entry in the dataframe via the `get_dataset_by_[name/doi]()` function. 



**Parameters:**
 *args: positional arguments  Positional arguments passed to the parent class constructor. hidden_column: str, optional  The name of the column to be hidden. **kwargs: keyword arguments  Keyword arguments passed to the parent class constructor. 



**Attributes:**
 hidden_column: str or None  The name of the hidden column. 

Methods: _repr_html_():  Overrides the _repr_html_ method of the parent class to hide the specified column in the HTML representation. get_dataset_by_name(dataset_name):  Returns the FoundryDataset associated with the given dataset name. Can also handle a DOI. get_dataset_by_doi(doi):  Returns the FoundryDataset associated with the given DOI. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(*args, hidden_column=None, **kwargs)
```






---

#### <kbd>property</kbd> T

The transpose of the DataFrame. 

Returns 
------- DataFrame  The transposed DataFrame. 

See Also 
-------- DataFrame.transpose : Transpose index and columns. 

Examples 
-------- ``` df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})```
``` df```  col1  col2 0     1     3 1     2     4 

``` df.T```
       0  1
col1  1  2
col2  3  4


---

#### <kbd>property</kbd> at

Access a single value for a row/column label pair. 

Similar to ``loc``, in that both provide label-based lookups. Use ``at`` if you only need to get or set a single value in a DataFrame or Series. 

Raises 
------ KeyError  If getting a value and 'label' does not exist in a DataFrame or Series. 

ValueError  If row/column label pair is not a tuple or if any label  from the pair is not a scalar for DataFrame.  If label is list-like (*excluding* NamedTuple) for Series. 

See Also 
-------- DataFrame.at : Access a single value for a row/column pair by label. DataFrame.iat : Access a single value for a row/column pair by integer  position. DataFrame.loc : Access a group of rows and columns by label(s). DataFrame.iloc : Access a group of rows and columns by integer  position(s). Series.at : Access a single value by label. Series.iat : Access a single value by integer position. Series.loc : Access a group of rows by label(s). Series.iloc : Access a group of rows by integer position(s). 

Notes 
----- See :ref:`Fast scalar value getting and setting <indexing.basics.get_value>` for more details. 

Examples 
-------- ``` df = pd.DataFrame([[0, 2, 3], [0, 4, 1], [10, 20, 30]],```
...                   index=[4, 5, 6], columns=['A', 'B', 'C'])
``` df```  A   B   C 4   0   2   3 5   0   4   1 6  10  20  30 

Get value at specified row/column pair 

``` df.at[4, 'B']```
2

Set value at specified row/column pair

``` df.at[4, 'B'] = 10``` ``` df.at[4, 'B']```
10

Get value within a Series

``` df.loc[5].at['B']``` 4 

---

#### <kbd>property</kbd> attrs

Dictionary of global attributes of this dataset. 

.. warning:
``` 

    attrs is experimental and may change without warning. 

```
See Also 
-------- DataFrame.flags : Global flags applying to this object. 

Notes 
----- Many operations that create new datasets will copy ``attrs``. Copies are always deep so that changing ``attrs`` will only affect the present dataset. ``pandas.concat`` copies ``attrs`` only if all input datasets have the same ``attrs``. 

Examples 
-------- For Series: 

``` ser = pd.Series([1, 2, 3])```
``` ser.attrs = {"A": [10, 20, 30]}``` ``` ser.attrs```
{'A': [10, 20, 30]}

For DataFrame:

``` df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})``` ``` df.attrs = {"A": [10, 20, 30]}```
``` df.attrs``` {'A': [10, 20, 30]} 

---

#### <kbd>property</kbd> axes

Return a list representing the axes of the DataFrame. 

It has the row axis labels and column axis labels as the only members. They are returned in that order. 

Examples 
-------- ``` df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})```
``` df.axes``` [RangeIndex(start=0, stop=2, step=1), Index(['col1', 'col2'], dtype='object')] 

---

#### <kbd>property</kbd> dtypes

Return the dtypes in the DataFrame. 

This returns a Series with the data type of each column. The result's index is the original DataFrame's columns. Columns with mixed types are stored with the ``object`` dtype. See :ref:`the User Guide <basics.dtypes>` for more. 

Returns 
------- pandas.Series  The data type of each column. 

Examples 
-------- ``` df = pd.DataFrame({'float': [1.0],```
...                    'int': [1],
...                    'datetime': [pd.Timestamp('20180310')],
...                    'string': ['foo']})
``` df.dtypes``` float              float64 int                  int64 datetime    datetime64[ns] string              object dtype: object 

---

#### <kbd>property</kbd> empty

Indicator whether Series/DataFrame is empty. 

True if Series/DataFrame is entirely empty (no items), meaning any of the axes are of length 0. 

Returns 
------- bool  If Series/DataFrame is empty, return True, if not return False. 

See Also 
-------- Series.dropna : Return series without null values. DataFrame.dropna : Return DataFrame with labels on given axis omitted  where (all or any) data are missing. 

Notes 
----- If Series/DataFrame contains only NaNs, it is still not considered empty. See the example below. 

Examples 
-------- An example of an actual empty DataFrame. Notice the index is empty: 

``` df_empty = pd.DataFrame({'A' : []})```
``` df_empty``` Empty DataFrame Columns: [A] Index: [] ``` df_empty.empty```
True

If we only have NaNs in our DataFrame, it is not considered empty! We
will need to drop the NaNs to make the DataFrame empty:

``` df = pd.DataFrame({'A' : [np.nan]})``` ``` df```
     A
0 NaN
``` df.empty``` False ``` df.dropna().empty```
True

``` ser_empty = pd.Series({'A' : []})``` ``` ser_empty```
A    []
dtype: object
``` ser_empty.empty``` False ``` ser_empty = pd.Series()```
``` ser_empty.empty``` True 

---

#### <kbd>property</kbd> flags

Get the properties associated with this pandas object. 

The available flags are 

* :attr:`Flags.allows_duplicate_labels` 

See Also 
-------- Flags : Flags that apply to pandas objects. DataFrame.attrs : Global metadata applying to this dataset. 

Notes 
----- "Flags" differ from "metadata". Flags reflect properties of the pandas object (the Series or DataFrame). Metadata refer to properties of the dataset, and should be stored in :attr:`DataFrame.attrs`. 

Examples 
-------- ``` df = pd.DataFrame({"A": [1, 2]})```
``` df.flags``` <Flags(allows_duplicate_labels=True)> 

Flags can be get or set using ``.`` 

``` df.flags.allows_duplicate_labels```
True
``` df.flags.allows_duplicate_labels = False``` 

Or by slicing with a key 

``` df.flags["allows_duplicate_labels"]```
False
``` df.flags["allows_duplicate_labels"] = True``` 

---

#### <kbd>property</kbd> iat

Access a single value for a row/column pair by integer position. 

Similar to ``iloc``, in that both provide integer-based lookups. Use ``iat`` if you only need to get or set a single value in a DataFrame or Series. 

Raises 
------ IndexError  When integer position is out of bounds. 

See Also 
-------- DataFrame.at : Access a single value for a row/column label pair. DataFrame.loc : Access a group of rows and columns by label(s). DataFrame.iloc : Access a group of rows and columns by integer position(s). 

Examples 
-------- ``` df = pd.DataFrame([[0, 2, 3], [0, 4, 1], [10, 20, 30]],```
...                   columns=['A', 'B', 'C'])
``` df```  A   B   C 0   0   2   3 1   0   4   1 2  10  20  30 

Get value at specified row/column pair 

``` df.iat[1, 2]```
1

Set value at specified row/column pair

``` df.iat[1, 2] = 10``` ``` df.iat[1, 2]```
10

Get value within a series

``` df.loc[0].iat[1]``` 2 

---

#### <kbd>property</kbd> iloc

Purely integer-location based indexing for selection by position. 

.. deprecated:: 2.2.0 

 Returning a tuple from a callable is deprecated. 

``.iloc[]`` is primarily integer position based (from ``0`` to ``length-1`` of the axis), but may also be used with a boolean array. 

Allowed inputs are: 


- An integer, e.g. ``5``. 
- A list or array of integers, e.g. ``[4, 3, 0]``. 
- A slice object with ints, e.g. ``1:7``. 
- A boolean array. 
- A ``callable`` function with one argument (the calling Series or  DataFrame) and that returns valid output for indexing (one of the above).  This is useful in method chains, when you don't have a reference to the  calling object, but would like to base your selection on  some value. 
- A tuple of row and column indexes. The tuple elements consist of one of the  above inputs, e.g. ``(0, 1)``. 

``.iloc`` will raise ``IndexError`` if a requested indexer is out-of-bounds, except *slice* indexers which allow out-of-bounds indexing (this conforms with python/numpy *slice* semantics). 

See more at :ref:`Selection by Position <indexing.integer>`. 

See Also 
-------- DataFrame.iat : Fast integer location scalar accessor. DataFrame.loc : Purely label-location based indexer for selection by label. Series.iloc : Purely integer-location based indexing for  selection by position. 

Examples 
-------- ``` mydict = [{'a': 1, 'b': 2, 'c': 3, 'd': 4},```
...           {'a': 100, 'b': 200, 'c': 300, 'd': 400},
...           {'a': 1000, 'b': 2000, 'c': 3000, 'd': 4000}]
``` df = pd.DataFrame(mydict)``` ``` df```
       a     b     c     d
0     1     2     3     4
1   100   200   300   400
2  1000  2000  3000  4000

**Indexing just the rows**

With a scalar integer.

``` type(df.iloc[0])``` <class 'pandas.core.series.Series'> ``` df.iloc[0]```
a    1
b    2
c    3
d    4
Name: 0, dtype: int64

With a list of integers.

``` df.iloc[[0]]```  a  b  c  d 0  1  2  3  4 ``` type(df.iloc[[0]])```
<class 'pandas.core.frame.DataFrame'>

``` df.iloc[[0, 1]]```  a    b    c    d 0    1    2    3    4 1  100  200  300  400 

With a `slice` object. 

``` df.iloc[:3]```
       a     b     c     d
0     1     2     3     4
1   100   200   300   400
2  1000  2000  3000  4000

With a boolean mask the same length as the index.

``` df.iloc[[True, False, True]]```  a     b     c     d 0     1     2     3     4 2  1000  2000  3000  4000 

With a callable, useful in method chains. The `x` passed to the ``lambda`` is the DataFrame being sliced. This selects the rows whose index label even. 

``` df.iloc[lambda x: x.index % 2 == 0]```
       a     b     c     d
0     1     2     3     4
2  1000  2000  3000  4000

**Indexing both axes**

You can mix the indexer types for the index and columns. Use ``:`` to
select the entire axis.

With scalar integers.

``` df.iloc[0, 1]``` 2 

With lists of integers. 

``` df.iloc[[0, 2], [1, 3]]```
       b     d
0     2     4
2  2000  4000

With `slice` objects.

``` df.iloc[1:3, 0:3]```  a     b     c 1   100   200   300 2  1000  2000  3000 

With a boolean array whose length matches the columns. 

``` df.iloc[:, [True, False, True, False]]```
       a     c
0     1     3
1   100   300
2  1000  3000

With a callable function that expects the Series or DataFrame.

``` df.iloc[:, lambda df: [0, 2]]```  a     c 0     1     3 1   100   300 2  1000  3000 

---

#### <kbd>property</kbd> loc

Access a group of rows and columns by label(s) or a boolean array. 

``.loc[]`` is primarily label based, but may also be used with a boolean array. 

Allowed inputs are: 


- A single label, e.g. ``5`` or ``'a'``, (note that ``5`` is  interpreted as a *label* of the index, and **never** as an  integer position along the index). 
- A list or array of labels, e.g. ``['a', 'b', 'c']``. 
- A slice object with labels, e.g. ``'a':'f'``. 

 .. warning:: Note that contrary to usual python slices, **both** the  start and the stop are included 


- A boolean array of the same length as the axis being sliced,  e.g. ``[True, False, True]``. 
- An alignable boolean Series. The index of the key will be aligned before  masking. 
- An alignable Index. The Index of the returned selection will be the input. 
- A ``callable`` function with one argument (the calling Series or  DataFrame) and that returns valid output for indexing (one of the above) 

See more at :ref:`Selection by Label <indexing.label>`. 

Raises 
------ KeyError  If any items are not found. IndexingError  If an indexed key is passed and its index is unalignable to the frame index. 

See Also 
-------- DataFrame.at : Access a single value for a row/column label pair. DataFrame.iloc : Access group of rows and columns by integer position(s). DataFrame.xs : Returns a cross-section (row(s) or column(s)) from the  Series/DataFrame. Series.loc : Access group of values using labels. 

Examples 
-------- **Getting values** 

``` df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],```
...                   index=['cobra', 'viper', 'sidewinder'],
...                   columns=['max_speed', 'shield'])
``` df```  max_speed  shield cobra               1       2 viper               4       5 sidewinder          7       8 

Single label. Note this returns the row as a Series. 

``` df.loc['viper']```
max_speed    4
shield       5
Name: viper, dtype: int64

List of labels. Note using ``[[]]`` returns a DataFrame.

``` df.loc[['viper', 'sidewinder']]```  max_speed  shield viper               4       5 sidewinder          7       8 

Single label for row and column 

``` df.loc['cobra', 'shield']```
2

Slice with labels for row and single label for column. As mentioned
above, note that both the start and stop of the slice are included.

``` df.loc['cobra':'viper', 'max_speed']``` cobra    1 viper    4 Name: max_speed, dtype: int64 

Boolean list with the same length as the row axis 

``` df.loc[[False, False, True]]```
             max_speed  shield
sidewinder          7       8

Alignable boolean Series:

``` df.loc[pd.Series([False, True, False],``` ...                  index=['viper', 'sidewinder', 'cobra'])]  max_speed  shield sidewinder          7       8 

Index (same behavior as ``df.reindex``) 

``` df.loc[pd.Index(["cobra", "viper"], name="foo")]```
        max_speed  shield
foo
cobra          1       2
viper          4       5

Conditional that returns a boolean Series

``` df.loc[df['shield'] > 6]```  max_speed  shield sidewinder          7       8 

Conditional that returns a boolean Series with column labels specified 

``` df.loc[df['shield'] > 6, ['max_speed']]```
             max_speed
sidewinder          7

Multiple conditional using ``&`` that returns a boolean Series

``` df.loc[(df['max_speed'] > 1) & (df['shield'] < 8)]```  max_speed  shield viper          4       5 

Multiple conditional using ``|`` that returns a boolean Series 

``` df.loc[(df['max_speed'] > 4) | (df['shield'] < 5)]```
             max_speed  shield
cobra               1       2
sidewinder          7       8

Please ensure that each condition is wrapped in parentheses ``()``.
See the :ref:`user guide<indexing.boolean>`
for more details and explanations of Boolean indexing.

.. note:
```
     If you find yourself using 3 or more conditionals in ``.loc[]``,
     consider using :ref:`advanced indexing<advanced.advanced_hierarchical>`.

     See below for using ``.loc[]`` on MultiIndex DataFrames.

```
Callable that returns a boolean Series

``` df.loc[lambda df: df['shield'] == 8]```  max_speed  shield sidewinder          7       8 

**Setting values** 

Set value for all items matching the list of labels 

``` df.loc[['viper', 'sidewinder'], ['shield']] = 50```
``` df```  max_speed  shield cobra               1       2 viper               4      50 sidewinder          7      50 

Set value for an entire row 

``` df.loc['cobra'] = 10```
``` df```  max_speed  shield cobra              10      10 viper               4      50 sidewinder          7      50 

Set value for an entire column 

``` df.loc[:, 'max_speed'] = 30```
``` df```  max_speed  shield cobra              30      10 viper              30      50 sidewinder         30      50 

Set value for rows matching callable condition 

``` df.loc[df['shield'] > 35] = 0```
``` df```  max_speed  shield cobra              30      10 viper               0       0 sidewinder          0       0 

Add value matching location 

``` df.loc["viper", "shield"] += 5```
``` df```  max_speed  shield cobra              30      10 viper               0       5 sidewinder          0       0 

Setting using a ``Series`` or a ``DataFrame`` sets the values matching the index labels, not the index positions. 

``` shuffled_df = df.loc[["viper", "cobra", "sidewinder"]]```
``` df.loc[:] += shuffled_df``` ``` df```
             max_speed  shield
cobra              60      20
viper               0      10
sidewinder          0       0

**Getting values on a DataFrame with an index that has integer labels**

Another example using integers for the index

``` df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],``` ...                   index=[7, 8, 9], columns=['max_speed', 'shield']) ``` df```
    max_speed  shield
7          1       2
8          4       5
9          7       8

Slice with integer labels for rows. As mentioned above, note that both
the start and stop of the slice are included.

``` df.loc[7:9]```  max_speed  shield 7          1       2 8          4       5 9          7       8 

**Getting values with a MultiIndex** 

A number of examples using a DataFrame with a MultiIndex 

``` tuples = [```
...     ('cobra', 'mark i'), ('cobra', 'mark ii'),
...     ('sidewinder', 'mark i'), ('sidewinder', 'mark ii'),
...     ('viper', 'mark ii'), ('viper', 'mark iii')
... ]
``` index = pd.MultiIndex.from_tuples(tuples)``` ``` values = [[12, 2], [0, 4], [10, 20],```
...           [1, 4], [7, 1], [16, 36]]
``` df = pd.DataFrame(values, columns=['max_speed', 'shield'], index=index)``` ``` df```
                      max_speed  shield
cobra      mark i           12       2
            mark ii           0       4
sidewinder mark i           10      20
            mark ii           1       4
viper      mark ii           7       1
            mark iii         16      36

Single label. Note this returns a DataFrame with a single index.

``` df.loc['cobra']```  max_speed  shield mark i          12       2 mark ii          0       4 

Single index tuple. Note this returns a Series. 

``` df.loc[('cobra', 'mark ii')]```
max_speed    0
shield       4
Name: (cobra, mark ii), dtype: int64

Single label for row and column. Similar to passing in a tuple, this
returns a Series.

``` df.loc['cobra', 'mark i']``` max_speed    12 shield        2 Name: (cobra, mark i), dtype: int64 

Single tuple. Note using ``[[]]`` returns a DataFrame. 

``` df.loc[[('cobra', 'mark ii')]]```
                max_speed  shield
cobra mark ii          0       4

Single tuple for the index with a single label for the column

``` df.loc[('cobra', 'mark i'), 'shield']``` 2 

Slice from index tuple to single label 

``` df.loc[('cobra', 'mark i'):'viper']```
                      max_speed  shield
cobra      mark i           12       2
            mark ii           0       4
sidewinder mark i           10      20
            mark ii           1       4
viper      mark ii           7       1
            mark iii         16      36

Slice from index tuple to index tuple

``` df.loc[('cobra', 'mark i'):('viper', 'mark ii')]```  max_speed  shield cobra      mark i          12       2  mark ii          0       4 sidewinder mark i          10      20  mark ii          1       4 viper      mark ii          7       1 

Please see the :ref:`user guide<advanced.advanced_hierarchical>` for more details and explanations of advanced indexing. 

---

#### <kbd>property</kbd> ndim

Return an int representing the number of axes / array dimensions. 

Return 1 if Series. Otherwise return 2 if DataFrame. 

See Also 
-------- ndarray.ndim : Number of array dimensions. 

Examples 
-------- ``` s = pd.Series({'a': 1, 'b': 2, 'c': 3})```
``` s.ndim``` 1 

``` df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})```
``` df.ndim``` 2 

---

#### <kbd>property</kbd> shape

Return a tuple representing the dimensionality of the DataFrame. 

See Also 
-------- ndarray.shape : Tuple of array dimensions. 

Examples 
-------- ``` df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})```
``` df.shape``` (2, 2) 

``` df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4],```
...                    'col3': [5, 6]})
``` df.shape``` (2, 3) 

---

#### <kbd>property</kbd> size

Return an int representing the number of elements in this object. 

Return the number of rows if Series. Otherwise return the number of rows times number of columns if DataFrame. 

See Also 
-------- ndarray.size : Number of elements in the array. 

Examples 
-------- ``` s = pd.Series({'a': 1, 'b': 2, 'c': 3})```
``` s.size``` 3 

``` df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})```
``` df.size``` 4 

---

#### <kbd>property</kbd> style

Returns a Styler object. 

Contains methods for building a styled HTML representation of the DataFrame. 

See Also 
-------- io.formats.style.Styler : Helps style a DataFrame or Series according to the  data with HTML and CSS. 

Examples 
-------- ``` df = pd.DataFrame({'A': [1, 2, 3]})```
``` df.style  # doctest: +SKIP``` 

Please see `Table Visualization <../../user_guide/style.ipynb>`_ for more examples. 

---

#### <kbd>property</kbd> values

Return a Numpy representation of the DataFrame. 

.. warning:
``` 

    We recommend using :meth:`DataFrame.to_numpy` instead. 

```
Only the values in the DataFrame will be returned, the axes labels will be removed. 

Returns 
------- numpy.ndarray  The values of the DataFrame. 

See Also 
-------- DataFrame.to_numpy : Recommended alternative to this method. DataFrame.index : Retrieve the index labels. DataFrame.columns : Retrieving the column names. 

Notes 
----- The dtype will be a lower-common-denominator dtype (implicit upcasting); that is to say if the dtypes (even of numeric types) are mixed, the one that accommodates all will be chosen. Use this with care if you are not dealing with the blocks. 

e.g. If the dtypes are float16 and float32, dtype will be upcast to float32.  If dtypes are int32 and uint8, dtype will be upcast to int32. By :func:`numpy.find_common_type` convention, mixing int64 and uint64 will result in a float64 dtype. 

Examples 
-------- A DataFrame where all columns are the same type (e.g., int64) results in an array of the same type. 

``` df = pd.DataFrame({'age':    [ 3,  29],```
...                    'height': [94, 170],
...                    'weight': [31, 115]})
``` df```  age  height  weight 0    3      94      31 1   29     170     115 ``` df.dtypes```
age       int64
height    int64
weight    int64
dtype: object
``` df.values``` array([[  3,  94,  31],  [ 29, 170, 115]]) 

A DataFrame with mixed type columns(e.g., str/object, int64, float32) results in an ndarray of the broadest type that accommodates these mixed types (e.g., object). 

``` df2 = pd.DataFrame([('parrot',   24.0, 'second'),```
...                     ('lion',     80.5, 1),
...                     ('monkey', np.nan, None)],
...                   columns=('name', 'max_speed', 'rank'))
``` df2.dtypes``` name          object max_speed    float64 rank          object dtype: object ``` df2.values```
array([['parrot', 24.0, 'second'],
        ['lion', 80.5, 1],
        ['monkey', nan, None]], dtype=object)




---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_dataset_by_doi`

```python
get_dataset_by_doi(doi)
```





---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_dataset_by_name`

```python
get_dataset_by_name(dataset_name)
```






---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Foundry`
Foundry Client Base Class 

This class represents a client for interacting with the Foundry service. It provides methods for searching and accessing datasets, as well as publishing new datasets. 



**Attributes:**
 
 - <b>`forge_client`</b> (Any):  The Forge client. 
 - <b>`connect_client`</b> (Any):  The MDF Connect client. 
 - <b>`transfer_client`</b> (Any):  The Globus transfer client. 
 - <b>`auth_client`</b> (Any):  The authentication client. 
 - <b>`index`</b> (str):  The index to use for search and data publication. 
 - <b>`auths`</b> (Any):  The authorizers used for authentication. 

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    no_browser: bool = False,
    no_local_server: bool = False,
    index: str = 'mdf',
    authorizers: dict = None,
    use_globus: bool = False,
    verbose: bool = False,
    interval: int = 10,
    parallel_https: int = 4,
    local_cache_dir: str = None,
    **data
)
```

Initialize a Foundry client 


---

#### <kbd>property</kbd> model_extra

Get extra fields set during validation. 



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`. 

---

#### <kbd>property</kbd> model_fields_set

Returns the set of fields that have been explicitly set on this model instance. 



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults. 



---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L484"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `check_status`

```python
check_status(source_id, short=False, raw=False)
```

Check the status of your submission. 



**Arguments:**
 
 - <b>`source_id`</b> (str):  The ``source_id`` (``source_name`` + version information) of the  submission to check. Returned in the ``res`` result from ``publish()`` via MDF Connect Client. 
 - <b>`short`</b> (bool):  When ``False``, will print a status summary containing  all of the status steps for the dataset.  When ``True``, will print a short finished/processing message,  useful for checking many datasets' status at once. 
 - <b>`**Default`</b>: ** ``False`` 
 - <b>`raw`</b> (bool):  When ``False``, will print a nicely-formatted status summary.  When ``True``, will return the full status result.  For direct human consumption, ``False`` is recommended. 
 - <b>`**Default`</b>: ** ``False`` 



**Returns:**
 
 - <b>`If ``raw`` is ``True``, *dict*`</b>:  The full status result. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L283"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `dataset_from_metadata`

```python
dataset_from_metadata(metadata: dict) → FoundryDataset
```

Converts the result of a forge query to a FoundryDatset object 



**Args:**
 
 - <b>`metadata`</b> (dict):  result from a forge query 



**Returns:**
 
 - <b>`FoundryDataset`</b>:  a FoundryDataset object created from the metadata 



**Raises:**
 
 - <b>`Exception`</b>:  If the mdf entry is missing a section, cannot generate a foundry dataset object 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L378"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `filter_datasets_by_query`

```python
filter_datasets_by_query(query_string: str, metadata: List[Dict]) → List[Dict]
```

Filters the given metadata based on the provided query string. 



**Args:**
 
 - <b>`query_string`</b> (str):  The query string to filter the metadata. 
 - <b>`metadata`</b> (list):  The list of metadata to be filtered. 



**Returns:**
 
 - <b>`list[dict]`</b>:  A list of dicts that match the query string. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L310"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_dataset`

```python
get_dataset(doi: str) → FoundryDataset
```

Get exactly one dataset by DOI 

Should only return a single result. 



**Args:**
 
 - <b>`doi`</b> (str):  doi of desired dataset 



**Returns:**
 
 - <b>`(FoundryDataset)`</b>:  A FoundryDataset loaded from the dataset metadata 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L329"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_metadata_by_doi`

```python
get_metadata_by_doi(doi: str) → dict
```

Query foundry datasets by DOI 

Should only return a single result. 



**Args:**
 
 - <b>`doi`</b> (str):  doi of desired dataset 



**Returns:**
 
 - <b>`metadata`</b> (dict):  result from a forge query 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L356"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_metadata_by_query`

```python
get_metadata_by_query(q: str, limit: int) → dict
```

Submit query to forge client and return results 



**Args:**
 
 - <b>`q`</b> (str):  query string  The query string to be submitted to the forge client. 
 - <b>`limit`</b> (int):  maximum number of results to return  The maximum number of results to be returned by the foundry client. 



**Returns:**
 
 - <b>`metadata`</b> (dict):  result from a forge query  The result from the forge query, represented as a dictionary. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L271"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list(limit: int = None, as_json: bool = False)
```

List available Foundry datasets 



**Args:**
 
 - <b>`limit`</b> (int):  maximum number of results to return 
 - <b>`as_json`</b> (bool):  If True, return results as list of dicts (agent-friendly) 



**Returns:**
 
 - <b>`List[FoundryDataset] or DataFrame or List[dict]`</b>:  Available datasets 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L415"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `publish_dataset`

```python
publish_dataset(
    foundry_dataset: FoundryDataset,
    update: bool = False,
    test: bool = False
)
```

Submit a dataset for publication via HTTPS using `local_data_path` or via Globus Transfer using the `globus_data_source` attribute. Only one upload method may be used. 



**Args:**
 
 - <b>`foundry_dataset`</b> (FoundryDataset):  The dataset to be published. 
 - <b>`update`</b> (bool):  True if this is an update to a prior data package. 
 - <b>`test`</b> (bool):  If True, do not submit the dataset for publication (i.e., transfer to the MDF endpoint).  Default is False. 



**Returns:**
 
 - <b>`dict`</b>:  MDF Connect Response. Response from MDF Connect to allow tracking  of dataset. Contains `source_id`, which can be used to check the  status of the submission. 



**Raises:**
 
 - <b>`ValueError`</b>:  If no data source is specified or if both data sources are specified. 

---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search`

```python
search(
    query: str = None,
    limit: int = None,
    as_list: bool = False,
    as_json: bool = False
) → List[FoundryDataset]
```

Search available Foundry datasets 

This method searches for available Foundry datasets based on the provided query string. If a DOI is provided as the query, it retrieves the metadata for that specific dataset. If a query string is provided, it retrieves the metadata for datasets that match the query. The limit parameter can be used to specify the maximum number of results to return. 



**Args:**
 
 - <b>`query`</b> (str):  The query string to match. If a DOI is provided, it retrieves the metadata for that specific dataset. 
 - <b>`limit`</b> (int):  The maximum number of results to return. 
 - <b>`as_list`</b> (bool):  If True, the search results will be returned as a list instead of a DataFrame. 
 - <b>`as_json`</b> (bool):  If True, return results as a list of dictionaries (agent-friendly). 



**Returns:**
 
 - <b>`List[FoundryDataset] or DataFrame or List[dict]`</b>:  Search results in the requested format. 



**Raises:**
 
 - <b>`Exception`</b>:  If no results are found for the provided query. 



**Example:**
 ``` foundry = Foundry()```
    >>> results = foundry.search(query="materials science", limit=10)
    >>> print(len(results))
    10


---

<a href="https://github.com/MLMI2-CSSI/foundry/tree/main/foundry/foundry.py#L395"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search_results_to_dataframe`

```python
search_results_to_dataframe(results)
```

Convert a list of results into a pandas DataFrame. 



**Args:**
 
 - <b>`results`</b> (list):  A list of results. 



**Returns:**
 
 - <b>`DataFrame`</b>:  A pandas DataFrame containing the converted results. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
