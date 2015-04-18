#!/usr/bin/env python
# coding=utf-8


def to_str(value):
    if isinstance(value, (type(None), str)):
        return value
    assert isinstance(value, unicode)
    return value.encode("utf-8")
