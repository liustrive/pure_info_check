#!/usr/bin/env python
# coding=utf-8
import jinja2

from config.config import config

class Template(object):

    def __init__(self,template_dir):
        auto_escape = config.get('autoescape',True)
        self.encoding = config.get('encoding','utf8')
        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir
            ),
            autoescape=auto_escape)
        
    def render(self,filename,kw={}):
        template = self._env.get_template(filename)
        return template.render(**kw).encode(self.encoding)
