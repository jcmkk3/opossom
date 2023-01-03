# opossum

opossum is an experimental API for data analysis. It is built on top of the very capable pandas library and is focused on API design ideas. It is very much a proof-of-concept and is not meant for use beyond general curiosity.

There are three different design ideas and each could be used on their own or replaced with a compatible design.

## Table

The `Table` object is designed around the idea of building pipelines of data operations which are preformed sequentially. This is an alternative to the method chaining style of most existing dataframe libraries like pandas. The advantage is that it is easy to pull apart and reuse pipelines. Favoring functions instead of methods also allows others to add additional functionality that gets first class treatment. Finally, it plays nicer with formatters like `black` which often reformat method chains in less nice ways. Any[^1] functions that could be used within a pandas `pandas.DataFrame.pipe` method, can be used as a step within the `Table`.

```python
# opossum
penguins[
    op.filter(col.num("flipper_length_mm") > 200),
    op.count("species"),
    op.slice()
]

# The pipeline can be extracted and reused
big_flipper_species = [
    op.filter(col.num("flipper_length_mm") > 200),
    op.count("species"),
    op.slice()
]

penguins[
    op.filter(col.str("island") == "Torgersen"),
    big_flipper_species,
]

# pandas equivalent
(
    penguins[lambda df: df["flipper_length_mm"] > 200]
    .value_counts("species")
    .reset_index(name="count")
    .head()
)
```

[^1]: Must return a dataframe or an object that can be coerced into a dataframe

## Verbs

Higher level verbs provide 'context' to how the computation should be performed. These 'verbs' are compatible with the `pandas.DataFrame.pipe` method, but are even more ergonimic to string together. These are largely inspired by grammar of data manipulation libraries like [dplyr](https://dplyr.tidyverse.org/) and [arquero](https://uwdata.github.io/arquero/).

Note that it is possible to use the verbs above with a pandas dataframe itself.

```python
# pandas with 'verbs'
(
    penguins
    .pipe(op.filter(col.num("flipper_length_mm") > 200))
    .pipe(op.count("species"))
    .pipe(op.slice())
)
```

## Column Expressions

Lastly, there are the column expression 'helpers'. These are compatible with any method in pandas that could accept a `lambda` function which takes a dataframe and returns a series or scalar. Many newer dataframe libraries like `polars` and `ibis` have an expression system. These allow a more natural expression of operations at the column level. In this case, I chose to make it required to specify the type (`col.num`/`col.str`) in order to get maximum help from autocompletion.

```python
# opossum
penguins[
    op.mutate({"upper_species": col.str("species").upper()})
]

# pandas
penguins.assign(upper_species=col.str("species").upper())

# lambda equivalent
penguins.assign(upper_species=lambda df: df["species"].str.upper())
```

## See More
- More usage of this API can be found in this [jupyter notebook](explore.ipynb)

## Future Ideas to Explore

- Could/should the `Table` or verbs be made compatible with scikit-learn's `transform`?
- Could/should the verbs accept any dataframe with a `__dataframe__` method, perform the computation and round trip back to the original type?
- Could/should their be a function that generates a schema object to be used as the expression namespace? (see [expression-namespace](/docs/expression-namespace.ipynb))

## License

`opossum` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
