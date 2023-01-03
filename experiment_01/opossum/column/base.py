from __future__ import annotations

from operator import attrgetter, itemgetter, methodcaller
import pandas


class Column:
    
    def __init__(self, funcs: str | list):
        if isinstance(funcs, str):
            self.funcs = [itemgetter(funcs)]
        else:
            self.funcs = funcs

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}({self.funcs!r})"

    def __call__(self, table):
        column = table

        for func in self.funcs:
            column = func(column)

        return column

    def __eq__(self, other):
        return self.__class__(self.funcs + [methodcaller("__eq__", other)])

    def __lt__(self, other):
        return self.__class__(self.funcs + [methodcaller("__lt__", other)])

    def __gt__(self, other):
        return self.__class__(self.funcs + [methodcaller("__gt__", other)])

    def __add__(self, other):
        return self.__class__(self.funcs + [methodcaller("__add__", other)])

    def __sub__(self, other):
        return self.__class__(self.funcs + [methodcaller("__sub__", other)])

    def __mul__(self, other):
        return self.__class__(self.funcs + [methodcaller("__mul__", other)])

    def __truediv__(self, other):
        return self.__class__(self.funcs + [methodcaller("__truediv__", other)])

    def __rtruediv__(self, other):
        return self.__class__(self.funcs + [methodcaller("__rtruediv__", other)])

    def __and__(self, other):
        return self.__class__(self.funcs + [methodcaller("__and__", other)])

    def __or__(self, other):
        return self.__class__(self.funcs + [methodcaller("__or__", other)])
    
    def __xor__(self, other):
        return self.__class__(self.funcs + [methodcaller("__xor__", other)])


def count():
    
    def inner(table):
        if isinstance(table, pandas.core.groupby.generic.DataFrameGroupBy):
            return pandas.Series(table.size(), name="count")
        
        return pandas.Series(table.size, name="count")
    
    return inner