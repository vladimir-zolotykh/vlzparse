# test_method_register.py

import pytest

from visitormulti import Method


def test_register_single_parameter():
    m = Method("visit")

    def f(self, x: int):
        pass

    m.register(f)

    assert m.methods == {
        (int,): f,
    }


def test_register_two_required_parameters():
    m = Method("visit")

    def f(self, x: int, y: str):
        pass

    m.register(f)

    assert m.methods == {
        (int,): f,
        (int, str): f,
    }


def test_register_one_optional_parameter():
    m = Method("visit")

    def f(self, x: int, y: str = "abc"):
        pass

    m.register(f)

    assert m.methods == {
        (int,): f,
        (int, str): f,
    }


def test_register_two_optional_parameters():
    m = Method("visit")

    def f(self, x: int, y: str = "abc", z: float = 1.0):
        pass

    m.register(f)

    assert m.methods == {
        (int,): f,
        (int, str): f,
        (int, str, float): f,
    }


def test_register_all_optional_parameters():
    m = Method("visit")

    def f(self, x: int = 1, y: str = "abc"):
        pass

    m.register(f)

    assert m.methods == {
        (): f,
        (int,): f,
        (int, str): f,
    }


def test_register_ignores_self():
    m = Method("visit")

    def f(self, x: int):
        pass

    m.register(f)

    assert (int,) in m.methods
    assert len(m.methods) == 1


def test_register_requires_annotation():
    m = Method("visit")

    def f(self, x):
        pass

    with pytest.raises(
        TypeError,
        match="All parameters must be annotated",
    ):
        m.register(f)


def test_register_requires_annotation_after_annotated_parameter():
    m = Method("visit")

    def f(self, x: int, y="abc"):
        pass

    with pytest.raises(
        TypeError,
        match="All parameters must be annotated",
    ):
        m.register(f)
