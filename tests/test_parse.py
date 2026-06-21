import pytest

from parser import Parser
import node as N


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        (
            "42",
            N.Num("42"),
        ),
        (
            "2+5",
            N.Plus(
                "+",
                N.Num("2"),
                N.Num("5"),
            ),
        ),
        (
            "3*4",
            N.Mul(
                "*",
                N.Num("3"),
                N.Num("4"),
            ),
        ),
        (
            "3+4*5",
            N.Plus(
                "+",
                N.Num("3"),
                N.Mul(
                    "*",
                    N.Num("4"),
                    N.Num("5"),
                ),
            ),
        ),
        (
            "(3+4)*5",
            N.Mul(
                "*",
                N.Plus(
                    "+",
                    N.Num("3"),
                    N.Num("4"),
                ),
                N.Num("5"),
            ),
        ),
        (
            "2+(3*4)+5",
            N.Plus(
                "+",
                N.Plus(
                    "+",
                    N.Num("2"),
                    N.Mul(
                        "*",
                        N.Num("3"),
                        N.Num("4"),
                    ),
                ),
                N.Num("5"),
            ),
        ),
    ],
)
def test_parse_valid(expr, expected):
    assert Parser().parse(expr) == expected
