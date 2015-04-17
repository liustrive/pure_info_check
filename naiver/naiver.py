#!/usr/bin/env python
# coding=utf-8
import logging
import Cookie

from config import config

logger = logging.getLogger('naiver')


class Application:
    """Create a basic wsgi application.
    """

    def __init__(self,url_mapping=(),vars={}):
        self._config = config._config
        self._urls = url_mapping

    def __call__(self, environ, start_response):
        self._status = '200 OK'
        self._headers = []
        output = route(environ)
        start_response()

    def route(self,environ):
        return ''

    def header_add(self,name,value):
        self._headers.append((name,value))

class HTTPRequest(object):
    
    def __init__(self,environ):
        pass
    
    def get_cookies():
        if not hasattr(self,"cookies"):
            self.cookies = Cookie.SimpleCookie()
            if self.envir_cookie:
                self.cookies.load(self.envir_cookie)
        return self.cookies

class RequestHandler(object):
    
    def __init__(self,app,request,**kwargs):
        self,app = app
        self.request = request
        
        self._headers = {"Content-Type": "text/html; charset=UTF-8"}
