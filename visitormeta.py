#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# flake8: noqa: F811
import inspect
from node import Node, Num, Plus, Minus, Mul, Div
from parser import Parser


class Register(dict):
    def __setitem__(self, key, val):
        # if key[:2] == '__' and key[-2:] == '__':
        #     super().__setitem__(key, val)
        if key.startswith("visit") and callable(val):
            sig = inspect.signature(val)
            parm = list[sig.parameters.values()][1]
            new_key = f"visit{parm.annotation.__name__}"  # visitNum
            super().__setitem__(new_key, val)
        else:
            super().__setitem__(key, val)


class VisitorMeta(type):
    def visit(self, n: Node):
        method_name = f"visis{type(n).__name__}"
        if hasattr(self, method_name):
            method = getattr(self, method_name)
        else:
            raise TypeError(f"{self.__class__} has no {method_name} method"
        return method(n)

    def __new__(mcls, clsname, bases, clsdict):
        clsdict["visit"] = visit
        return super().__new__(mcls, clsname, bases, clsdict)

    @classmethod
    def __prepare__(name, bases, **kwargs):
        return Register()


class VisitorDispatch(metaclass=VisitorMeta):
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
    print(VisitorDispatch().visit(Parser().parse(expr)))
