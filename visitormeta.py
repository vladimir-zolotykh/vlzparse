#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# flake8: noqa: F811
# mypy: disable-error-code="no-redef"
from typing import MutableMapping, Any
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
    @classmethod
    def __prepare__(
        mcls, clsname: str, bases: tuple[type, ...], /, **kwargs: Any
    ) -> MutableMapping[str, object]:
        return Register()


class Visitor:
    def visit(self, n: Node) -> float:
        self.method_name = f"visit{type(n).__name__}"
        method = getattr(self, self.method_name, self.visit_generic)
        return method(n)

    def visit_generic(self, n: Node) -> float:
        raise TypeError(f"{self.__class__} has not {self.method_name}")


class VisitorDispatch(Visitor, metaclass=VisitorMeta):
    def visit(self, n: Num) -> float:
        return float(n.val)

    def visit(self, n: Plus) -> float:
        return self.visit(n.left) + self.visit(n.right)

    def visit(self, n: Minus) -> float:
        return self.visit(n.left) - self.visit(n.right)

    def visit(self, n: Mul) -> float:  # noqa: F811
        return self.visit(n.left) * self.visit(n.right)

    def visit(self, n: Div) -> float:  # noqa: F811
        return self.visit(n.left) / self.visit(n.right)


if __name__ == "__main__":
    expr = "2 + (3 * 4) + 5"
    print(f"{expr = }, {eval(expr) = }")
    v = VisitorDispatch()
    print(v.visit(Parser().parse(expr)))
