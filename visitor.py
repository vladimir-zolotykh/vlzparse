#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Generic, TypeVar, cast, Callable

# from functools import singledispatchmethod
import node as N
from parser import Parser

T = TypeVar("T")


class Visitor(Generic[T]):
    def visit(self, n: N.Node) -> float:
        self.method_name = f"visit{type(n).__name__}"
        method = cast(
            Callable[[N.Node], float],
            getattr(self, self.method_name, self.visitGeneric),
        )
        return method(n)

    def visitGeneric(self, n: N.Node) -> float:
        raise NotImplementedError(
            f"{self.__class__.__name__} doesn't implement {self.method_name}"
        )


class VisitorEval(Visitor[float]):
    def visitNum(self, n: N.Num) -> float:
        return float(n.val)

    def visitPlus(self, n: N.Plus) -> float:
        return self.visit(n.left) + self.visit(n.right)

    def visitMinus(self, n: N.Minus) -> float:
        return self.visit(n.left) - self.visit(n.right)

    def visitMul(self, n: N.Mul) -> float:
        return self.visit(n.left) * self.visit(n.right)

    def visitDiv(self, n: N.Div) -> float:
        return self.visit(n.left) / self.visit(n.right)


if __name__ == "__main__":
    expr = "2 + (3 * 4) + 5"
    print(f"{expr = }, {eval(expr) = }")
    print(VisitorEval().visit(Parser().parse(expr)))
