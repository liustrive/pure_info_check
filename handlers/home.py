#!/usr/bin/env python
# coding=utf-8
import os

from naiver import utils
from naiver import naiver
from common.infoService import InfoService

class Home(naiver.RequestHandler):
    def get(self):
        data={'fellows':''}
        return self.respond('info.html',data)

    def post(self):
        name = self.request.get('name')
        if not name:
            name=''
        print name
        info_serv = InfoService()
        fellows = info_serv.show_info(name)
        data = {'fellows':fellows,'search_name':name.decode('utf8')}
        return self.respond('info.html',data)
