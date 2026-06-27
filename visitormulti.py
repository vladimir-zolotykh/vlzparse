#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# mypy: disable-error-code=no-redef
from typing import MutableMapping, Any, Callable, get_type_hints
from types import MethodType
import inspect
from node import Num, Plus, Minus, Mul, Div, Node
from parser import Parser


class MethodTup:
    def __init__(self, name):
        self._name = name
        self.methods = {}

    def register(self, func):
        sig = inspect.signature(func)
        _types: tuple[type, ...] = tuple()
        for k, p in sig.parameters.items():
            if k == "self":
                continue
            if p.annotation is inspect._empty:
                raise TypeError("All parameters must be annotated")
            if p.default is not inspect._empty:
                self.methods[_types] = func
            _types = _types + (p.annotation,)
            self.methods[_types] = func

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def __call__(self, *args):
        _types = tuple(type(a) for a in args[1:])
        return self.methods[_types](*args)


def bind_typed(sig: inspect.Signature, *args, **kwargs) -> inspect.BoundArguments:
    ba = sig.bind(*args, **kwargs)
    ba.apply_defaults()

    for name, value in ba.arguments.items():
        param = sig.parameters[name]
        ann = param.annotation

        if ann is inspect._empty:
            continue

        if not isinstance(value, ann):
            raise TypeError(
                f"{name}: expected {ann.__name__}, got {type(value).__name__}"
            )

    return ba


class MethodSig:
    def __init__(self, name):
        self._name = name
        self.signatures: list[Callable] = []

    def register(self, func):
        self.signatures.append(func)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        sig: inspect.Signature
        func: Callable
        for func in self.signatures:
            try:
                sig: inspect.Signature = inspect.signature(func)
                for name, parm in sig.parameters.items():
                    if name == "self":
                        continue
                    if parm.annotation is inspect._empty:
                        raise TypeError(
                            f"All parameters of {func.__name__} must be annotated"
                        )
                    ba = bind_typed(sig, *args, **kwargs)
                    return func(*ba.args, **ba.kwargs)
            except TypeError:
                pass
        raise TypeError(f"No matching {args} method {self._name} found") from exc


# Method = MethodTup
Method = MethodSig


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
