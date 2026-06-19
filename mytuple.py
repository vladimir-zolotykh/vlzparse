#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(cls, name, bases, namespace)
        fields = namespace.get("_fields", [])
        for n, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(n)))


class Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args):
        if len((n := len(cls._fields))) != len(args):
            raise TypeError(f"{cls} gets exactly {n} arguments")
        return super().__new__(cls, args)


class Person(Tuple):
    _fields = ["name", "age", "salary"]


def as_csv(p: Person) -> str:
    return ", ".join(f"{name}={getattr(p, name)!r}" for name in p._fields)


if __name__ == "__main__":
    p = Person("Bob", 37, 12000)
    print(repr(p))
    print(as_csv(p))
