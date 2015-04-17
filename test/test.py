#!/usr/bin/env python
# coding=utf-8
from wsgiref.simple_server import make_server, demo_app

def my_app(environ,start_response):
    """
    hello app to test environment setup
    """
    status = '200 OK'
    response_headers = [('Content-Type','text/plain')]
    start_response(status,response_headers)
    return ['Works fun!\n']

httpd = make_server('',8086,my_app)
sa = httpd.socket.getsockname()
print 'http://{0}:{1}'.format(*sa)

httpd.serve_forever()
