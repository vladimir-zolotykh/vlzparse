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


class Plus(BinaryOp):
    def __repr__(self):
        return f"Plus({self.left}, {self.right})"


class Minus(BinaryOp):
    def __repr__(self):
        return f"Minus({self.left}, {self.right})"


class Mul(BinaryOp):
    def __repr__(self):
        return f"Mul({self.left}, {self.right})"


class Div(BinaryOp):
    pass
