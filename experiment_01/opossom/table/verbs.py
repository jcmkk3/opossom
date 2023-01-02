from typing import Callable

import pandas


def select(*column_names):
    column_names = list(column_names)

    def inner(table):
        return table[column_names]

    return inner


def slice_(*args, **kwargs):
    to_slice = slice(5)

    if args or kwargs:
        to_slice = slice(*args, **kwargs)

    def inner(table):
        return table[to_slice]

    return inner


def filter_(func, by=None):
    if isinstance(by, str):
        by = [by]

    def inner(table):
        if by:
            table = table.groupby(by)

        return table[func]

    return inner


def sort(*column_names, reverse=False):
    column_names = list(column_names)
    ascending = not reverse

    def inner(table):
        return table.sort_values(by=column_names, ascending=ascending)

    return inner


def rename(mapper, /):
    if not isinstance(mapper, Callable):
        mapper = {v: k for k, v in dict(mapper).items()}

    def inner(table):
        return table.rename(columns=mapper)

    return inner


def mutate(funcs, by=None):
    def inner(table):
        return table.assign(**funcs)

    return inner


def rollup(funcs, by=None):
    if by is None:
        by = []

    if isinstance(by, str):
        by = [by]

    def inner(table):
        if by:
            table = table.groupby(by)

        table = pandas.concat(
            [pandas.Series(func(table), name=name) for name, func in funcs.items()],
            axis="columns",
        ).reset_index(by)

        return table

    return inner


def count(*column_names):
    column_names = list(column_names)

    def inner(table):
        if not column_names:
            return pandas.Series(len(table), name="count")

        return table.value_counts(column_names).reset_index(name="count")

    return inner


def dropna(*column_names, how="any"):
    column_names = list(column_names)
    
    if not column_names:
        column_names = None

    def inner(table):
        return table.dropna(how=how, subset=column_names)

    return inner


def fillna(*column_names, value=None, method=None):
    column_names = list(column_names)

    def inner(table):
        if not column_names:
            table = table.fillna(value=value, method=method)

        table = table.assign(
            **{
                col: table[col].fillna(value=value, method=method)
                for col in column_names
            }
        )

        return table

    return inner
