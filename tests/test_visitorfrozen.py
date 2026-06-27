import pytest

from visitorfrozen import Evaluator
from node import Num, Plus, Minus, Mul, Div


@pytest.fixture
def ev():
    return Evaluator()


def test_visit_num(ev):
    assert ev.visit(Num(3)) == 3.0


def test_visit_plus(ev):
    assert ev.visit(Plus(Num(2), Num(3))) == 5.0


def test_visit_minus(ev):
    assert ev.visit(Minus(Num(5), Num(2))) == 3.0


def test_visit_mul(ev):
    assert ev.visit(Mul(Num(4), Num(3))) == 12.0


def test_visit_div(ev):
    assert ev.visit(Div(Num(8), Num(2))) == 4.0


def test_visit_nested_expression(ev):
    expr = Plus(
        Num(2),
        Mul(Num(3), Num(4)),
    )
    assert ev.visit(expr) == 14.0
