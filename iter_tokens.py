#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re
from dataclasses import dataclass


@dataclass
class Token:
    name: str
    val: str | float
    par: str


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

if __name__ == "__main__":
    print(tokens)
