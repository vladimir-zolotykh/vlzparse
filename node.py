#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Any
from dataclasses import dataclass


@dataclass
class Node:
    val: Any
    left: Node
    right: Node


class Num(Node):
    pass


@dataclass
class BinaryOp(Node):
    pass


class Plus(BinaryOp):
    pass


class Minus(BinaryOp):
    pass


class Mul(BinaryOp):
    pass


class Div(BinaryOp):
    pass
