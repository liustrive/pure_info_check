#!/usr/bin/env python
# coding=utf-8
import sys
import re

__all__ = ["RouterExcetion","Router"]

class RouterException(Exception):
    pass

 
class Router(object):

    def __init__(self,urls=[],vars={}):
        self._urls = urls
        self._vars = vars

    def get(self,path,method):
        for pattern, handlerName in self._urls:
            m = re.match('^' + pattern + '$',path)
            if m:
                args = m.groups()
                cls = self._vars.get(handlerName)
                if hasattr(cls,method.lower()):
                    return cls,args
        raise RouterException(
            "Request method not found: %s" % method)
    
    def add_path(self,path,handler):
        pass
