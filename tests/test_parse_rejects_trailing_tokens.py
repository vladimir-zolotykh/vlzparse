import pytest
from parser import Parser


@pytest.mark.parametrize(
    "expr",
    [
        "1 2",
        "1+2 3",
        "(1)2",
        "1(2)",
    ],
)
def test_parse_rejects_trailing_tokens(expr):
    with pytest.raises(SyntaxError):
        Parser().parse(expr)
