#!/usr/bin/env python
# coding=utf-8
from wsgiref.simple_server import make_server

from naiver import naiver
from handlers.home import Home


urls = [('/','Home'),('/index','Home')]
app = naiver.Application(urls,globals())
if __name__ == "__main__":
    httpd = make_server('127.0.0.1',6969,app)
    httpd.serve_forever()
