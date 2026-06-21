#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Any
from dataclasses import dataclass


@dataclass
class Node:
    val: Any


@dataclass
class Num(Node):
    def __repr__(self):
        return f"Num({self.val})"


@dataclass
class BinaryOp(Node):
    left: Node | None = None
    right: Node | None = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left}, {self.right})"


class Plus(BinaryOp):
    pass


class Minus(BinaryOp):
    pass


class Mul(BinaryOp):
    pass


class Div(BinaryOp):
    pass
