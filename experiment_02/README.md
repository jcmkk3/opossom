Entry Points
============

There are two primary entry points: `table` and `column`
These are typically aliased as `tbl` and `col`.
```python
>>> import opossom.table as tbl
>>> import opossom.column as col
```

Table construction always happens with the `tbl.Table` object.
```python
>>> fruits = tbl.Table(
...    {"name": ["apple", "orange", "banana"], "color": ["red", "orange", "yellow"]}
... )
>>> inventory = tbl.Table(
...     [
...         {"item": "computer", "quantity": 11},
...         {"item": "printer", "quantity": -2},
...         {"item": "scanner", "quantity": 6}
...     ]
... )
>>> penguins = tbl.Table.from_csv("data/penguins.csv")
```

Usage Template
==============

Typical usage follows the following template:
```
table = tbl.Table.from_<source>(...)

table.<table method>(
    tbl.<table verb>(
        col[<column name>].<column transformation>
    )
)
```

Examples:
```python
penguins = tbl.Table.from_csv("data/penguins.csv")

penguins.query(
    tbl.count(by="species")
)

penguins.query(
    tbl.rollup(col["body_mass_g"].mean(), by="species")
)
```

Here are some useful methods on the `tbl.Table` object.
These typically return a different object so are not intended to be chained.
```python
# Prints a tabular representation of table (by default with a `limit 10`)
>>> penguins.peak(
...     tbl.select(...), tbl.filter(...), ...
... )
species   island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g  sex     year
-------   ------  --------------  -  ------------  -----------------  -----------  ---     ----
Gentoo    Biscoe            46.7           15.3                219         5200  male    2007
Adelie    Biscoe            39.7           17.7                193         3200  female  2009
Gentoo    Biscoe            46.4           15.                 216         4700  female  2008
Adelie    Torgersen         38.6           21.2                191         3800  male    2007
Gentoo    Biscoe            43.8           13.9                208         4300  female  2008
Gentoo    Biscoe            48.8           16.2                222         6000  male    2009
Adelie    Dream             36.8           18.5                193         3500  female  2009
Chinstrap Dream             49.8           17.3                198         3675  female  2009
Adelie    Dream             36.            18.5                186         3100  female  2007
Adelie    Dream             39.5           17.8                188         3300  female  2007

# Prints compact representation of table, especially good for many columns
>>> penguins.glimpse(
...     tbl.select(...), tbl.filter(...), ...
... )
species: Gentoo, Adelie, Gentoo, Adelie, Gentoo, Gentoo, Adelie, Chinstrap
island: Biscoe, Biscoe, Biscoe, Torgersen, Biscoe, Biscoe, Dream, Dream, Dream
bill_length_mm: 46.7, 39.7, 46.4, 38.6, 43.8, 48.8, 36.8, 49.8, 36., 39.5, 48.4
bill_depth_mm: 15.3, 17.7, 15., 21.2, 13.9, 16.2, 18.5, 17.3, 18.5, 17.8, 14.4
flipper_length_mm: 219, 193, 216, 191, 208, 222, 193, 198, 186, 188, 203, 200
body_mass_g: 5200, 3200, 4700, 3800, 4300, 6000, 3500, 3675, 3100, 3300, 4625 
sex: male, female, female, male, female, male, female, female, female, female
year: 2007, 2009, 2008, 2007, 2008, 2009, 2009, 2009, 2007, 2007, 2009, 2008

# Prints result of performing explain
>>> penguins.explain(
...     tbl.select(...), tbl.filter(...), ...
... )

# Returns results as a new `Table` object backed by in-memory arrow table
>>> penguins.query(
...     tbl.select(...), tbl.filter(...), ...
... )

# Returns summary statistics as a new `Table` object backed by in-memory arrow table
>>> penguins.describe(
...     tbl.select(...), tbl.filter(...), ...
... )

# Returns a dictionary (or custom object) representing the table''s schema
>>> penguins.schema()

# Returns the number of rows in the table
>>> len(penguins)
```

Table Verbs
===========
- `select`
- `update`
- `rollup`
- `filter`
- `sort`
- `slice`
- `sample`
- `shuffle`
- `pivot`
- ...

The other methods in the `tbl` module are to be used within the methods on a `tbl.Table` instance.
These provide instructions for performing high-level transformations of the data.
Each method can be thought of as representing a complete `select ... from table ...` in SQL.
A sequence of verbs can be thought as multiple SQL `with` statements with each subsequent statement referencing the previous statement.
```python
>>> fruits.query(
...     tbl.select("name"),
... )
>>> fruits.query(
...     tbl.rename({"name": "fruit_name", "color": "fruit_color"}),
... )
>>> fruits.query(
...     tbl.sort("name"),
...     tbl.slice(2),
... )
```

Column Transformations
======================

The methods on the `col` object are typically column helpers that don't reference a specific column in the dataset.
```python
>>> fruits.query(
...     tbl.rollup(col.count()),
... )
>>> fruits.query(
...     tbl.rollup(col.all().is_empty().count()),
... )
>>> fruits.query(
...     tbl.select(col.not(starts_with="c")),
... )
>>> fruits.query(
...     tbl.update(col.join("name", "color", sep=", ")),
... )
>>> penguins.query(
...     tbl.update(col.ratio("height", to="width")),
... )
>>> penguins.query(
...     tbl.filter(
...         col.any(
...             col["name"].endswith("apple"),
...             col["color"] == "red",
...         ),
...     ),
... )

```

When using the `__getitem__` method, a field object is returned.
These are used to provide instructions for how to manipulate a colum.
These methods can be chained and can always be expected to return a new `tbl.Column` object at the end.
```python
>>> fruits.query(
...     tbl.update(col["name"].upper()),
... )
>>> fruits.query(
...     tbl.rollup(col["color"].len().mean())
... )
```

Most text editors will not be able to understand which methods are applicable to the datatype of the column that you are operating on.
When you first try to use a method after specifying a field name, your editor will try to give you all methods available to all datatypes.
Once you use a method, subsequent methods that you try to chain will be narrowed down to only those that could be used with the previous method.
```python
>>> col["name"].
#               ^^^ will offer all column methods as completion options
>>> col["name"].upper().
#                       ^^^ will only offer methods for strings as `upper` only works on strings
```


If a single string is passed to the `__getitem__` method of a `tbl.Table` instance, it will return a column for that field.
The column names should be available as completion options since they are known.
That column will have only the methods of its column type available since the datatype of the column is known at this time.
```python
>>> fruits["color"].title()
>>> penguins["species"].distinct()
>>> fruits["name"] + " - " + fruits["color"]
```


Design Motivations
==================
Designed to make it as easy as possible to get data ingested into the library
- In most cases, reading from a csv or excel file poses the most challenging since those formats are so unrestricted.
  Most of the method options in pandas or readr can be reduced if you allow the verbs in the read function itself.
  Need to rename some columns?
  ```python
  penguins = tbl.Table.from_csv(
    "data/penguins.csv",
    tbl.rename(...),
    tbl.update(col.all(col.Str).na_if("NA"),
  )
  ```


Designed for local data first


Designed for interactive usage first


Reduce 3rd party dependencies where possible


Easy delimiting of eager vs lazy.
```python
>>> penguins.query(op.update(...), op.filter(...), op.sample(...), op.select(...), ...)
#                  <---        everything within the parenthesis can be lazy       --->
```

With a method chaining style of transformation pipelines, there needs to be a special method (`execute`, `collect`, etc.) that materializes the data.

```python
>>> fruits["name"].title()
>>> col["name"].title()
#   ^^^ just swap the table name for the `col` object and it becomes lazy, to be used in the context of a lazy table like above
```


Easily refactor.
```python
>>> penguins.glimpse(tbl.update(...), tbl.filter(...), tbl.sample(...), ...)
>>> transforms = [tbl.update(...), tbl.filter(...), tbl.sample(...), ...]
>>> penguins.glimpse(transforms, ...)
>>> penguins.to_parquet(transforms, path="data/penguins.parquet", partition="egg_year")
>>> tbl.Table.from_parquet(
...     tbl.filter(col["egg_year"] > 2010),
...     path="data/penguins.parquet",
... )

>>> penguins["species"].split(" ", n=1)[0]  # Get it right in an eager way
>>> penguins.query(tbl.update(col["species"].split(" ", n=1)[0]))  # Then use it within a pipeline
>>> short_species = col["species"].split(" ", n=1)[0]  # OR Assign the transformation to a variable
>>> penguins.query(tbl.update(short_species), ...)  # Then use it in as many pipelines as needed

>>> penguins.query(tbl.count(by="species"))
>>> penguins.query(tbl.rollup(col.count(), col["weight"].mean(), by="species")]
#                      ^^^ just change to another method that can be grouped and add the additional arguments
```

- Can easily split a single `tbl` method out or a sequence of `tbl` methods or a chain of `col` methods
- If you want it to be parameterized, then create a function. It should be just a normal function that returns a `tbl` or `col` derived object

Plays well with modern python style (i.e. black)
TODO: opossom vs method chaining style
TODO: how it is easier to reformat from a single line to multiple
TODO: how it is possble to force multiline for ease of reading


Make it easy to discover actions that can be performed.
```python
>>> tbl.
#       ^^^ should offer all functions that can be performed within a `tbl.Table` instance's pipeline methods

>>> col[...].
#            ^^^ should offer all methods that can be performed on a named column

>>> col.
#       ^^^ should offer all column related methods that do not operate on a single named column

>>> tbl.Table.from_
#                  ^^^ should offer all alternative constructor methods

>>> tbl.Table(...).to_
#                    ^^^ should offer all conversion methods

>>> tbl.Table(...).
#                  ^^^ all pipeline methods and properties
```


Should have simple imports.
```python
>>> import opossom.table as tbl
>>> import opossom.column as col
```
This goes along with the discovery note above.
This is especially important for a library that will often be used interactively.


Should be easy to extend.
```python
>>> tbl.Table(...).query(my_function())
#                        ^^^ using functions here instead of methods makes it easy for others to use their functions in a pipeline

>>> tbl.update(geocol[...].latitude(), col["species"].title())
#              ^^^ since the `col` object is separate from the primary table object, it is pretty seamless to use a separate parent object for a custom column type
```
New data classes can be created in the same way that one would typically create a class in python. Data will typically be stored in a struct and all methods on the class will return a sqlglot AST. This includes custom `__repr__` that is shown when printing a table.

Example classes:
- Units like celsius, farenheight, cm, mm, inches, etc.
  These would have methods to be able to convert between unit types
- Money (usd, pound, euro, yen, etc.)
- Inflated money. something like https://github.com/palewire/cpi, but datatypes
  Would be able to compare revenue or cost from different time periods in a normalized way
- A color class that can output a color in rbg, hex, hsl, etc or do transformations on colors, repr could even show the color
- Geography
- Paths, URLs
- Business objects with defined logic

- These could have rich `__str__` methods that would show the most relavent information in an easy to consume way.
  How information is displayed is extremely important in this context
- Could use format mini language to allow customization of how the values appear on-the-fly (change `__str__` output)

Advantage is that there could be alternative constructor methods on the class that was specific to how your data shows up.
```python
>>> account.from_str("account")
# Stored in a struct with fields `client` and `business_unit`
>>> account["account"].client
>>> account["account"].business_unit
>>> account["account"].format()  # Show as string
```

It could also be useful when working with a denormalized data source to roll up multiple columns into an easier to deal with column like a user (user_id, name, email, phone number).

These could be thought of like dimensions in dimensional modeling except with the ability to attach specific functionality to them. You could even map existing dimension tables to a custom data type, if you'd like. How the data is actually stored when it is being worked with is dependent on the engine used (sqlite, duckdb, datafusion, etc) and whether it is being done in memory or using an existing database on disk.


What about completion of column names?
I felt that methods were much more important to complete. Column names are easy to reference if needed. There are so many methods and remembering all of the arguments would be difficult. 

Future: could be a schema object with the building blocks

Future: could be extension/package for editors to help with column name completion

Current: can start by working on a column in eager mode where it will be completed and offer completion only for column type.


Why is there no column access through attributes?
- While `__getitem__` syntax is a bit more clunky, it is much more consistent and flexible than using attribute lookup
- Column names do not need to be a valid python identifer
- There is no need to worry about methods clashing with the column names
- It is easier to identify where column names are being referenced since the `col[..]` syntax stands out
- There is an expectation that attributes should be offered as completion, but it is not possible with lazy objects that do not know which columns are available in the table. There is not that same expectation with the `__getitem__` method.


Why not use accessors for different datatypes like pandas
```python
>>> pd.DataFrame(...)["string column"].str.split(" ", n=1, expand=True)[0].str.title()
#                                      ^^^                                 ^^^
```
- It is cumbersome to type an accessor before every method that you need to use.
- String and date methods are very common and it is not unusual to need to chain multiple operations.
- After using a single method, the type system should be able to have a pretty good idea about what type the column represents.
- Functions are all global in database systems so there is not a need to have namespacing in the python representation for name conflict reasons.
- It is no worse than functional oriented analysis languages like R and Julia.
- Advantage of the accessors is that it is easy to see the functions that are available on a type.
- Advantage of the accessors is that the completion list to scroll through could be shorter.
- The tradeoff is reducing typing and visual clutter at the cost of some discoverability, but there are ways to make up for it somewhat:
```python
>>> col.ColumnStr("string column").
#                                  ^^^ offers only completion for string types
>>> data["string column"].
#                         ^^^ knows the column's datatype so will only offer relevant completions
```

Why use methods vs functions for operation on columns?
- Python is pragmatic in its use of functions and methods.
- Numeric types typically use functions and other types use methods.
- Columns of a table are really a combination of the container and value types.
- It is probably not advantageous to try to emulate python's approach in this case since there's not a literal representation of these types.


Why is `by` (group by) a keyword argument instead of a function/method?
TODO: talk about general avoidance of fluent builder style APIs (`case` and `if` are other examples).


How are the column names are generated for column expressions?
- All expressions are given implicit names.
  This allows for better interactive use.
- Most methods do not change the name of the base column, it is modified
- Aggregate methods append the aggregate name to the column name
- Multi-column methods (including operators) generate new column names
- Any column can be explicitly named by using the `.as_(...)` method


Implementation
==============
- `duckdb` is the primary computational engine that the library is built around
- It uses `sqlglot` as an abstraction layer above the computational engine
  This provides the possibility of using the API with other computational engines that can speak SQL
- Each `tbl` function is typically represented as a CTE (`with` statement) in the SQL output
  This makes it very easy to read and reason about, while aligning with the modern analytical SQL style
TODO: Example of sql output with `show_sql` (or whatever it is to be called) method
- The `query` method, as well as some others, generate a new `Table` instance that is backed by an arrow table
- All needed types to document functions should be included in the main namespaces
  - Should these be protocols, abstract types, or concrete types?


Ideas
=====
Does it make sense to give some less obvious names or aliases to the `table` and `column` modules/objects to reduce the chance that they would accidentally be overwritten?
- `tl`, `cl`
- `pouch`, `joey`  # bad, but something cutesy/nonsensical *could* be fine
- ...

Options for pipeline syntax
```python
>>> penguins[tbl.update(...), ...]  # __getitem__ syntax
```
- Advantage is that it gives all of the method/property real estate of the `Table` object for non-querying operations
- Advantage is that it communicates that the operations are happening inside of the `Table` object
- Advantage is that it is very simple to see the relation between the square bracket `Table(...)[...]` syntax and a list. Just remove the table object and you have refactored the pipeline to a list.
- Disadvantage is that it is uncommon to do so much with the `__getitem__` method. Especially being able to pass in functions
- Disadvantage is that unpacking (`*iterable`) is not supported between the brackets
- Disadvantage is that keyword arguments are not supported between the brackets

```python
>>> penguins(tbl.update(...), ...)  # it could be `__call__` instead
```
- Advantage is that it would be possible to use unpacking (`*iterable`)
- Advantage is that it would be possible to add additional keyword arguments, if needed
- Advantage is would make `__getitem__` syntax solely for materializing a single column in an eager fashion

```python
>>> penguins.query(tbl.update(...), ...)  # could just use a method call
>>> penguins.glimpse(tbl.update(...), ...)
>>> penguins.explain(tbl.update(...), ...)
>>> ...
```
- Advantage is that it would be possible to use unpacking (`*iterable`)
- Advantage is that it would be possible to add additional keyword arguments, if needed
- Advantage is would make `__getitem__` syntax solely for materializing a single column in an eager fashion
- Advantage is that user could switch the method and have the same call signature for different context
- Advantage is that method call are most idomatic
- Advantage is that method calls look best if multiple pipelines will be chained for some reason
- Disadvantage is that it makes all usage more verbose
- Disadvantage is that it makes a single line of transformations undesirable as it would be too hard to parse by looking

It would probably be suggested to always make a multiline expression even if there was just a single `tbl` transform
The nice part is that it wouldn't require any reformatting of the code to extend the transformation pipeline
```python
>>> penguins.query(
>>>     tbl.count(...),
>>> ) 
```


Should there be some bailout methods that allow string SQL queries?
```python
>>> penguins.query(tbl.sql("select *"))  # could accept a string query in addition to `tbl` functions
>>> col.sql("upper(species)")
```


The eager column extraction takes away from the easy extension argument
```python
>>> col["string column"].
>>> geo["custom geo column"].  # can easily use a custom object along with the default `col`
>>> penguins["string column"].
>>> penguins["custom geo column"].  # the `tbl.Table` object would need to know about the new data type for this to work
```

- What is a custom data type in the context of a database anyways?
- Could be implemented as an extension like in sqlite.
- Could be represented as a struct in the database. Compound functions could be created to make working with it easy.
- What parts of the API will most likely need extended?
  - IO: there will always be new file or database sources that would be useful to connect to. The same can be said for output, but those might be more constrained.
  - How should that affect the API?
    Maybe it starts with a `connect`, `read`, `write` type of API that is a shortcut to the common methods and options using file extensions and URIs.
    All methods (as well as externally added) would have dedicated functions in `connect`, `read`, `write` submodules
- Is there a logical/clean way to map the various SQL language constructs to the API?
    - Table valued functions
    - Aggregate functions
    - Scalar functions
    - etc
- Reshaping functions should probably accept a function to rename the columns/values. For instance, I'd always want to create columns that are valid python identifiers and not some with strange characters or spaces.
- Should there be a `set` data type 
- HTML repr could copy code to access a certain row or data point to clipboard when you click on it.
- Should there be separate classes for different table sources?
```python
>>> tbl.Table  # Parent type
>>> tbl.TableCSV(...)
>>> tbl.TableExcel(...)
>>> tbl.TableParquet(...)
>>> tbl.TableDuckDB(...)
>>> tbl.TableSQLite(...)
>>> tbl.TablePostgres(...)

>>> penguins = tbl.TableCSV(
...     "data/penguins.csv",
...     tbl.rename(str.lower)
... )
```

- Can/should users add metadata to any of the objects (table or column)?
- Perform a query with a log or step through tbl steps: something like [tidylog](https://github.com/elbersb/tidylog) or [datamations](https://github.com/microsoft/datamations). Could just be a verbose flag on some other method.


Relation to other tools in pydata ecosystem
===========================================
numpy
pandas
scikit-learn
matplotlib
seaborn
pytorch


Inspirations
============
- tidyverse
- ibis
- arquero
- SQL
- qSQL (from Q language/kdb+)
- M (from Power Query/Power BI)
- malloy


Naming things
=============
Considerations
- Write the doc string first. It might reveal what wording will make the most sense.
- Names should be idiomatic to python if possible
- Is the name a verb, adverb, noun, adjective?
- How quickly will it be narrowed using code completion?
  Multiple names on the same object that have a common root are undesirable unless they actually perform the same task
- Shorter is typically better, but not at a huge sacrifice to understanding
- Keep in mind when there are operations that have an opposite that makes sense.
  Those should choose names that work well in that context.

Potential Names
- Getting distinct values: distinct, unique, drop_duplicates, remove_duplicates
- Checking if values are null: isna, isnull, isempty
- Subsetting a range of rows based on a predicate: filter, where, keep, discard
- Getting a range of rows: head, limit, slice
- Getting a random range of rows: sample
- Getting the generated SQL (or other generated code): show_sql
- Getting a view of some rows of data: glimpse, show, view, peek, inspect, limit
- Modifying or adding columns: mutate, assign, derive, transform, update (Q, Shakti)
- Outputting to a file (or database?): to_*, write_*, from_*, write, export, dump(s)
- Plotting the data: plot
- Rename/alias a column: as_, name, alias
- Scan/Accumulation using +: cumsum, sums (from Q)
- Joining data: join_one, join_many, join_anti, join_semi
