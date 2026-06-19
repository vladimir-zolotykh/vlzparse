#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Any
from inspect import Parameter, signature, Signature
from operator import itemgetter


class TupleMeta(type):
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        fields = namespace.get("_fields", [])
        parms = [
            Parameter(name, Parameter.POSITIONAL_OR_KEYWORD, annotation=Any)
            for name in fields
        ]
        if parms:
            cls.__signature__ = Signature(parms)

        return cls

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        fields = namespace.get("_fields", [])
        for n, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(n)))


class Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args):
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"{cls} gets exactly {n} arguments")
        return super().__new__(cls, args)


class Person(Tuple):
    _fields = ["name", "age", "salary"]


def as_csv(p: Person) -> str:
    return ", ".join(f"{name}={getattr(p, name)!r}" for name in p._fields)


if __name__ == "__main__":
    print(signature(Person))
    p = Person("Bob", 37, 12000)
    print(repr(p))
    print(as_csv(p))
    try:
        Person("Jim", 38)
    except TypeError as exc:
        print(exc)
