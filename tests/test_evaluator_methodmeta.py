# test_evaluator.py

import pytest

from visitormulti import Evaluator
from parser import Parser
from node import Num, Plus, Minus, Mul, Div


@pytest.fixture
def ev():
    return Evaluator()


def test_num(ev):
    assert ev.visit(Num(42)) == 42.0


def test_plus(ev):
    node = Plus("+", Num(2), Num(3))
    assert ev.visit(node) == 5.0


def test_minus(ev):
    node = Minus("-", Num(7), Num(4))
    assert ev.visit(node) == 3.0


def test_mul(ev):
    node = Mul("*", Num(6), Num(7))
    assert ev.visit(node) == 42.0


def test_div(ev):
    node = Div("/", Num(8), Num(2))
    assert ev.visit(node) == 4.0


def test_nested_expression(ev):
    # 2 + (3 * 4)
    node = Plus(
        "+",
        Num(2),
        Mul("*", Num(3), Num(4)),
    )

    assert ev.visit(node) == 14.0


def test_complex_expression(ev):
    # (10 - 2) * (9 / 3)
    node = Mul(
        "*",
        Minus("-", Num(10), Num(2)),
        Div("/", Num(9), Num(3)),
    )

    assert ev.visit(node) == 24.0


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("1", 1.0),
        ("2+3", 5.0),
        ("10-4", 6.0),
        ("6*7", 42.0),
        ("8/2", 4.0),
        ("2+3*4", 14.0),
        ("(2+3)*4", 20.0),
        ("2+(3*4)+5", 19.0),
        ("20/(2*5)", 2.0),
    ],
)
def test_parser_integration(ev, expr, expected):
    tree = Parser().parse(expr)
    assert ev.visit(tree) == expected


def test_division_by_zero(ev):
    node = Div("/", Num(1), Num(0))

    with pytest.raises(ZeroDivisionError):
        ev.visit(node)
