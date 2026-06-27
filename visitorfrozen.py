#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import MutableMapping, Any, Callable
from types import MethodType
import inspect
from node import Num, Plus, Minus, Mul, Div
from parser import Parser


class Method:
    def __init__(self, name):
        self._name = name
        self.methods: dict[str, Callable] = {}

    def register(self, func):
        sig = inspect.signature(func)
        types: tuple[type, ...] = ()
        for name, parm in sig.parameters.items():
            if name == "self":
                continue
            if parm.annotation is inspect._empty:
                raise TypeError(f"All parameters of {self.__name__} must be annotated")
            types = types + (parm.annotation,)
        self.methods[types] = func

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        types: tuple[type, ...] = tuple(type(a) for a in args[1:])
        return self.methods[types](*args)


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


class MethodFrozen(type):
    @classmethod
    def __prepare__(
        mcls, clsname: str, bases: tuple[type, ...], /, **kwargs: Any
    ) -> MutableMapping[str, object]:
        return Map()


class Evaluator(metaclass=MethodFrozen):
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
