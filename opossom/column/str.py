from __future__ import annotations

from operator import attrgetter, itemgetter, methodcaller

from .base import Column


class StrColumn(Column):
    def upper(self) -> StrColumn:
        return self.__class__(self.funcs + [attrgetter("str"), methodcaller("upper")])

    def title(self) -> StrColumn:
        return self.__class__(self.funcs + [attrgetter("str"), methodcaller("title")])

    def lower(self) -> StrColumn:
        return self.__class__(self.funcs + [attrgetter("str"), methodcaller("lower")])
    
    def isin(self, values) -> StrColumn:
        return self.__class__(self.funcs + [methodcaller("isin", values)])


def str_(name: str) -> StrColumn:
    return StrColumn(name)
