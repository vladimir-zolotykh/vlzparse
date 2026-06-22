#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Any, ClassVar
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
    left: Node
    right: Node

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left}, {self.right})"


class _BinaryOp(BinaryOp):
    op: ClassVar[str]

    def __init__(self, left, right):
        super().__init__(self.op, left, right)


class Plus(_BinaryOp):
    op = "+"


class Minus(_BinaryOp):
    op = "-"


class Mul(_BinaryOp):
    op = "*"


class Div(_BinaryOp):
    op = "/"
