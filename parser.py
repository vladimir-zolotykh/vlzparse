#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import iter_tokens as T
import node as N


class Parser:
    def __init__(self):
        self.token: T.Token | None = None

    def _advance(self) -> T.Token | None:
        try:
            self.token = next(self.tokens)
        except StopIteration:
            self.token = None
        return self.token

    def _expect(self, expected: str) -> None:
        if not self.token == expected:
            raise SyntaxError(f"Expected {expected}, got {self.token}")
        self._consume()

    def _consume(self) -> None:
        self.token = next(self.tokens)

    def expr(self) -> N.Node:
        res: N.Node = self.term()
        while (op := self.token) and op in ("PLUS", "MINUS"):
            self._consume()
            right = self.term()
            res = N.Plus(res, right) if op == "PLUS" else N.Minus(res, right)
        return res

    def term(self) -> N.Node:
        res: N.Node = self.factor()
        while (op := self.token) and op in ("MUL", "DIV"):
            self._consume()
            right = self.factor()
            res = N.Mul(res, right) if op == "MUL" else N.Div(res, right)
        return res

    def factor(self) -> N.Node:
        res: N.Node
        if self.token is None:
            raise SyntaxError("Token expected")
        elif self.token == "LPAREN":
            self._consume()
            res = self.expr()
            self._expect("RPAREN")
        else:
            res = N.Num(self.token.val)
            self._advance()
        return res

    def parse(self, expr: str) -> N.Node:
        self.tokens: Iterator[T.Token] = T.iter_tokens(expr)
        self._advance()
        return self.expr()


if __name__ == "__main__":
    expr = "2 + (3 * 4) + 5"
    # expr = "2 + 5"
    # expr = "3 * 4"
    # expr = "3 + 4 * 5"
    print(f"{expr = }, {eval(expr) = }")
    n = Parser().parse(expr)
    print(n)
