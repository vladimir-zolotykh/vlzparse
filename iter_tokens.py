#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import re
from dataclasses import dataclass


@dataclass
class Token:
    name: str
    val: str | float


tokens = {
    key: rf"(?P<{key}>{val})"
    for key, val in {
        "NAME": r"[A-Za-z][A-Za-z0-9_]*",
        "PLUS": r"\+",
        "MINUS": r"\-",
        "MUL": r"\*",
        "DIV": r"/",
        "EQ": r"=",
        "LPAREN": r"\(",
        "RPAREN": r"\)",
        "NUM": r"\d+",
        "WS": r"\s+",
    }.items()
}


def iter_tokens(expr: str) -> Iterator[Token]:
    pat = "|".join(tokens.values())
    for match in re.finditer(pat, expr):
        name = match.lastgroup
        if name != "WS":
            yield Token(name, match.group(0))


if __name__ == "__main__":
    for t in iter_tokens("2 + (3 * 4) + 5"):
        print(t)
