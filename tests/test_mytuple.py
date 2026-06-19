import pytest
from mytuple import Person, as_csv
import inspect


def test_person():
    assert str(inspect.signature(Person)) == "(name: Any, age: Any, salary: Any)"
    p = Person("Bob", 37, 12000)
    assert repr(p) == "('Bob', 37, 12000)"
    assert as_csv(p) == "name='Bob', age=37, salary=12000"
    with pytest.raises(TypeError, match=r".*\.Person'> gets exactly 3 arguments"):
        Person("Jim", 37)
