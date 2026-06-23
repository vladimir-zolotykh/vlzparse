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
        # if key[:2] == '__' and key[-2:] == '__':
        #     super().__setitem__(key, val)
        if key == "visit" and callable(val):
            sig = inspect.signature(val)
            # parm = list[sig.parameters.values()][1]
            types_ = [p.annotation for p in sig.parameters.values()]
            new_key = f"visit{types_[1].__name__}"  # visitNum
            super().__setitem__(new_key, val)
        else:
            super().__setitem__(key, val)


class VisitorMeta(type):

    def __new__(mcls, clsname, bases, clsdict):
        # def visit(self, n: Node):
        #     method_name = f"visit{type(n).__name__}"
        #     if hasattr(self, method_name):
        #         method = getattr(self, method_name)
        #     else:
        #         raise TypeError(f"{self.__class__} has no {method_name} method")
        #     return method(n)

        # clsdict["visit"] = visit
        return super().__new__(mcls, clsname, bases, clsdict)

    @classmethod
    def __prepare__(
        mcls, clsname: str, bases: tuple[type, ...], /, **kwargs: Any
    ) -> MutableMapping[str, object]:
        return Register()


class Visitor:
    def visit(self, n: Node):
        self.method_name = f"visit{type(n).__name__}"
        method = getattr(self, self.method_name, self.visit_generic)
        return method(n)

    def visit_generic(self, n: Node):
        raise TypeError(f"{self.__class__} has not {method_name}")


class VisitorDispatch(Visitor, metaclass=VisitorMeta):
    def visit(self, n: Num) -> float:
        return float(n.val)

    def visit(self, n: Plus) -> float:
        return self.visit(n.left) + self.visit(n.right)

    def visit(self, n: Minus) -> float:
        return self.visit(n.left) - self.visit(n.right)

    def visit(self, n: Mul) -> float:
        return self.visit(n.left) * self.visit(n.right)

    def visit(self, n: Div) -> float:
        return self.visit(n.left) / self.visit(n.right)


if __name__ == "__main__":
    expr = "2 + (3 * 4) + 5"
    print(f"{expr = }, {eval(expr) = }")
    v = VisitorDispatch()
    print(v.visit(Parser().parse(expr)))
