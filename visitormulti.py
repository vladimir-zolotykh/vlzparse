#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# mypy: disable-error-code=no-redef
from typing import MutableMapping, Any
from types import MethodType
import inspect
from node import Num, Plus, Minus, Mul, Div
from parser import Parser


class Method:
    def __init__(self, name):
        self._name = name
        self.methods = {}

    def register(self, func):
        sig = inspect.signature(func)
        _types: tuple[type, ...] = tuple()
        typesdefault: tuple[type, ...] = tuple()
        for k, p in sig.parameters.items():
            if k == "self":
                continue
            if p.annotation is inspect._empty:
                raise TypeError("All parameters must be annotated")
            _types = _types + (p.annotation,)
            if p.default is inspect._empty:
                typesdefault = typesdefault + (p.annotation,)
                self.methods[typesdefault] = func
        self.methods[_types] = func

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def __call__(self, *args):
        _types = tuple(type(a) for a in args[1:])
        return self.methods[_types](*args)


class Map(dict):
    def __setitem__(self, key, val):
        if key not in self:
            super().__setitem__(key, val)
            return
        oval = self[key]
        if isinstance(oval, Method):
            mm: Method = oval
            oval.register(val)
        else:
            mm = Method(key)
            mm.register(oval)
            mm.register(val)
        super().__setitem__(key, mm)


class MethodMeta(type):
    @classmethod
    def __prepare__(
        mcls, clsname: str, bases: tuple[type, ...], /, **kwargs: Any
    ) -> MutableMapping[str, object]:
        return Map()


class Evaluator(metaclass=MethodMeta):
    def visit(self, n: Num) -> float:
        return float(n.val)

    def visit(self, n: Plus) -> float:  # noqa: F811
        return self.visit(n.left) + self.visit(n.right)  # type: ignore[arg-type]

    def visit(self, n: Minus) -> float:  # noqa: F811
        return self.visit(n.left) - self.visit(n.right)  # type: ignore[arg-type]

    def visit(self, n: Mul) -> float:  # noqa: F811
        return self.visit(n.left) * self.visit(n.right)  # type: ignore[arg-type]

    def visit(self, n: Div) -> float:  # noqa: F811
        return self.visit(n.left) / self.visit(n.right)  # type: ignore[arg-type]


if __name__ == "__main__":
    expr = "2 + (3 * 4) + 5"
    print(f"{expr = }, {eval(expr) = }")
    print(Evaluator().visit(Parser().parse(expr)))  # type: ignore[arg-type]
