#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import singledispatchmethod
from node import Node, Num, Plus, Minus, Mul, Div
from parser import Parser


class VisitorDispatch:
    @singledispatchmethod
    def visit(self, n: Node) -> float:
        raise NotImplementedError(
            f"{self.__class__.__name__} doesn't implement visit({type(n)})"
        )

    @visit.register
    def _(self, n: Num) -> float:
        return float(n.val)

    @visit.register
    def _(self, n: Plus) -> float:
        return self.visit(n.left) + self.visit(n.right)

    @visit.register
    def _(self, n: Minus) -> float:
        return self.visit(n.left) - self.visit(n.right)

    @visit.register
    def _(self, n: Mul) -> float:
        return self.visit(n.left) * self.visit(n.right)

    @visit.register
    def _(self, n: Div) -> float:
        return self.visit(n.left) / self.visit(n.right)


if __name__ == "__main__":
    expr = "2 + (3 * 4) + 5"
    print(f"{expr = }, {eval(expr) = }")
    print(VisitorDispatch().visit(Parser().parse(expr)))
