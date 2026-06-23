#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# mypy: disable-error-code="no-redef"
from typing import MutableMapping, Any, TYPE_CHECKING
import inspect
from node import Node, Num, Plus, Minus, Mul, Div
from parser import Parser


class Register(dict):
    def __setitem__(self, key, val):
        if key == "visit" and callable(val):
            sig = inspect.signature(val)
            types_ = [p.annotation for p in sig.parameters.values()]
            new_key = f"visit{types_[1].__name__}"  # visitNum
            super().__setitem__(new_key, val)
        else:
            super().__setitem__(key, val)


class VisitorMeta(type):
    def __new__(mcls, name, bases, ns):
        ns2 = dict(ns)
        ns2["visit"] = mcls._visit
        ns2["visit_generic"] = mcls._visit_generic
        return super().__new__(mcls, name, bases, ns2)

    def _visit(self, n: Node) -> float:
        method_name = f"visit{type(n).__name__}"
        method = getattr(self, method_name, self.visit_generic)
        return method(n)

    def _visit_generic(self, n: Node) -> float:
        raise TypeError(
            f"{self.__class__.__name__} has not " f"visit{type(n).__name__}"
        )

    @classmethod
    def __prepare__(
        mcls, clsname: str, bases: tuple[type, ...], /, **kwargs: Any
    ) -> MutableMapping[str, object]:
        return Register()


if not TYPE_CHECKING:

    class VisitorDispatch(metaclass=VisitorMeta):
        def visit(self, n: Num) -> float:
            return float(n.val)

        def visit(self, n: Plus) -> float:  # noqa: F811
            return self.visit(n.left) + self.visit(n.right)

        def visit(self, n: Minus) -> float:  # noqa: F811
            return self.visit(n.left) - self.visit(n.right)

        def visit(self, n: Mul) -> float:  # noqa: F811
            return self.visit(n.left) * self.visit(n.right)

        def visit(self, n: Div) -> float:  # noqa: F811
            return self.visit(n.left) / self.visit(n.right)


if __name__ == "__main__":
    expr = "2 + (3 * 4) + 5"
    print(f"{expr = }, {eval(expr) = }")
    print(VisitorDispatch().visit(Parser().parse(expr)))
