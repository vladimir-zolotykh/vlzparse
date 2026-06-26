#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# mypy: disable-error-code=no-redef
from typing import MutableMapping, Any, Callable
from types import MethodType
import inspect
from node import Num, Plus, Minus, Mul, Div
from parser import Parser


class MethodSig:
    def __init__(self, name):
        self._name = name
        self.signatures: list[tuple[inspect.Signature, Callable]] = []

    def register(self, func):
        self.signatures.append((inspect.signature(func), func))

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def __call__(self, *args):
        sig: inspect.Signature
        func: Callable
        for sig, func in self.signatures:
            try:
                ba: inspect.BoundArguments = sig.bind(*args)
                ba.apply_defaults()
                return func(*ba.args)
            except TypeError:
                continue  # try next (sig, func) in signatures
        raise TypeError(f"No matching method {self._name} for {ba}")


class Map(dict):
    def __setitem__(self, key, val):
        if key not in self:
            super().__setitem__(key, val)
            return
        oval = self[key]
        if isinstance(oval, MethodSig):
            mm: MethodSig = oval
            oval.register(val)
        else:
            mm = MethodSig(key)
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
