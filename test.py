#!/usr/bin/env python
# coding=utf-8
import os

from naiver import naiver

class Home(naiver.RequestHandler):
    def get(self):
        return 'It works.'

urls = [('/index',"Home")]
app = naiver.Application(urls)

if __name__ == '__main__':
    print ''
    handler = naiver.RequestHandler()


