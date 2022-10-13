from __future__ import annotations

from operator import attrgetter, itemgetter, methodcaller

from .base import Column


class NumColumn(Column):
    def sum(self) -> NumColumn:
        return self.__class__(self.funcs + [methodcaller("sum")])

    def mean(self) -> NumColumn:
        return self.__class__(self.funcs + [methodcaller("mean")])


def num(name: str) -> NumColumn:
    return NumColumn(name)
