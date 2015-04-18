#!/usr/bin/env python
# coding=utf-8
import logging
import Cookie

from config import config
import router

__all__ = [ "Application", "HTTPRequest", "RequestHandler", "RequestHandler","ErrorHandler" ]

logger = logging.getLogger('naiver')

class Application:
    """Create a basic wsgi application.
    """

    def __init__(self,url_mapping=(),vars={}):
        self._config = config._config
        self._urls = url_mapping
        self._vars = vars
        self._router = Router(url_mapping,vars)

    def __call__(self, environ, start_response):
        
        request = HTTPRequest(environ)
        response = self.route(request)
        start_response(response.status,response.headers)
        # just for test
        #body = "It works. just for test"
        #headers= [('Content-type','text/plain')]
        #response = HTTPResponse(body)
        #start_response(response.status,response.headers)
        return response.body

    def route(self,request):
        try:
            handlercls,args = self._router.get(
                request.path,request.method)
        except RouterException:
            return ErrorHandler.show(404)
        handlerIns = handlercls(self, request)
        method = getattr(handlerIns,request.method.lower())
        if args:
            return method(handlerIns,args)
        else:
            return method()


class ErrorHandler(RequestHandler):
    
    def __init__(self):
        self.error_dict = {
            404:'Page not found'
        }
    
    def show(self, errorcode):
        pass

class HTTPRequest(object):
    
    def __init__(self,environ):
        self._env = environ
        pass
    
    def get_cookies(self):
        if not hasattr(self,"cookies"):
            self.cookies = Cookie.SimpleCookie()
            if self.envir_cookie:
                self.cookies.load(self.envir_cookie)
        return self.cookies
    def get(self):
        """get args"""
        pass

    @property
    def get_path(self):
        """get url path"""
        if 'PATH_INFO' in self._env:
            return self._env['PATH_INFO']
        logger.error('No path_info set in wsgi.environ')
        return None
    
    @property
    def get_headers(self):
        if not hasattr(self,'_headers'):
            self._headers = {}
            for k,v in self._env:
                if k.startswith('HTTP'):
                    self._headers[k] = v
        return self._headers

class HTTPResponse(object):
    def __init__(self,body,status=200):
        self._headers = [('Content-Type','text/html; charset=UTF-8')]
        self._status = '200 OK'
        self._cookies = None
        self._body = body

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self,name,value):
        self._headers[name] = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,value):
        self._status = value

    @property
    def body(self):
        return self._body
    
    @body.setter
    def body(self,value):
        self._body = value

        
class RequestHandler(object):
    
    def __init__(self,app,request,**kwargs):
        self,app = app
        self.request = request
        if not hasattr(self,"response"):
            self.response = HTTPResponse()

    def respond(self,file,data):
        #TODO
        pass

    def text_respond(self,data):
        self.response._headers = [('Content-Type','text/plain')]
        self.response.body = data
        return self.response
