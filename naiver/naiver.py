#!/usr/bin/env python
# coding=utf-8
import logging
import Cookie
import urlparse

import utils
from config import config
from router import Router,RouterException
from template import Template
__all__ = [ "Application","HTTPRequest", \
           "RequestHandler","RequestHandler",\
           "ErrorHandler" ]

logger = logging.getLogger('naiver')



class HTTPRequest(object):
    
    def __init__(self,environ):
        self._env = environ
        self._args = {}
        self._cookies = None

    @property
    def cookies(self):
        if not self._cookies:
            self._cookies =  Cookie.SimpleCookie(
                self._env.get('HTTP_COOKIE',''))
        return self._cookies

    def args_get(self):
        request_query = urlparse.parse_qs(self._evn['QUERY_STRING'])
        self._args = dict()
        for k,v in request_query:
            self._args[k] = v
        return self._args
    
    def args_post(self):
        content_length = int(self._env.get('CONTENT_LENGH'),0)
        request_body = self._env['wsgi.input'].read(content_length)
        body_parsed = urlparse.parse_qs(request_body)
        self._args = dict()
        for k,v in body_parsed:
            self._args[k] = v
        return self._args

    def get(self,key,default = None):
        """get args"""
        if self._args:
            return self._args.get(key,default)
        if self.method.upper()=='GET':
            self.args_get().get(key,default)
        else:
            self.args_post().get(key,default)


    @property
    def path(self):
        """get url path"""
        if 'PATH_INFO' in self._env:
            return self._env['PATH_INFO']
        logger.error('No path_info set in wsgi.environ')
        return None

    @property
    def method(self):
        return self._env.get('REQUEST_METHOD','GET')

    @property
    def get_headers(self):
        if not hasattr(self,'_headers'):
            self._headers = {}
            for k,v in self._env:
                if k.startswith('HTTP'):
                    self._headers[k] = v
        return self._headers

class HTTPResponse(object):
    
    def __init__(self,cookie=None,body='',status=200):
        self._headers = [('Content-Type','text/html; charset=UTF-8')]
        self._status = '200 OK'
        self._cookies = cookie
        self._body = body

    @property
    def cookies(self):
        if not self._cookies:
            self._cookies = Cookie.SimpleCookie()
        return self._cookies

    def set_cookie(self,key,value):
        self.cookies[key] = value

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self,name,value):
        self._headers[name] = utils.to_str(value)

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
        self._body = utils.to_str(value)

        
class RequestHandler(object):
    
    def __init__(self,app=None,request=None,**kwargs):
        self._app = app
        self._request = request
        if not hasattr(self,"response"):
            self._response = HTTPResponse()
        self._template = Template(config.config.get('template_dir'))

    def respond(self,file,data):
        self._response.body = self._template.render(file,data)
        return self._response

    def text_respond(self,data):
        self._response._headers = [('Content-Type','text/plain')]
        self._response.body = data
        return self._response

    @property
    def request(self):
        return self._request

    @property
    def app(self):
        return self._response

class ErrorHandler(RequestHandler):
    
    def __init__(self):
        self.error_dict = {
            404:'Page not found'
        }
    
    def show(self, errorcode):
        RequestHandler.__init__(self)
        return self.text_respond('page not found')

class Application:
    """Create a basic wsgi application.
    """

    def __init__(self,url_mapping=(),vars={}):
        self._config = config.config
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
            handler= ErrorHandler()
            return handler.show(404)
        handlerIns = handlercls(self, request)
        method = getattr(handlerIns,request.method.lower())
        if args:
            return method(handlerIns,args)
        else:
            return method()
