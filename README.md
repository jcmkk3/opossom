# opossum

opossum is a space to experiment with APIs for data analysis in python.


Here's a taste of the most recent (v2) API design brainstorm:

```python
import opossum.table as tbl
import opossum.column as col

penguins = tbl.Table.from_csv("data/penguins.csv")

penguins.query(
    tbl.count(by="species")
)

penguins.query(
    tbl.drop_duplicates(),
    tbl.rollup(col["body_mass_g"].mean(), by="species")
)

penguins.to_parquet("data/penguins.csv", partition="egg_date")
```


## Experiments
- [opossum v1](experiment_01/README.md)
- [opossum v2](experiment_02/README.md)

Mini
- [column namespace](mini_experiments/column-namespace.ipynb)
- [expression namespace](mini_experiments/expression-namespace.ipynb)


## License

`opossum` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
