#!/usr/bin/env python
# coding=utf-8
import os

from naiver import naiver
from common.infoService import InfoService
from common import lib

class AddInfo(naiver.RequestHandler):
    def get(self):
        info_serv = InfoService()
        groups = info_serv.get_groups()
        data={'groups':groups}
        return self.respond('addinfo.html',data)

    def post(self):
        name = self.request.get('name')
        sex = self.request.get('sex')
        popo = self.request.get('popo')
        groups = self.request.get('group')
        print name,sex,popo,groups
        if not name or not sex or not popo or not groups:
            msg = '请填写完整表单'
            data = {'server_msg':msg.decode('utf8')}
            return self.respond('addinfo.html',data)

        #TODO info check
        if sex.isdigit() and groups.isdigit():
            sex=int(sex)
            groups=int(groups)
        else:
            msg = '数据校验失败'
            data={'server_msg':msg.decode('utf8')}
            return self.respond('addinfo.html',data)

        print 'post inputs：%s,%d,%s,%d' % (name,sex,popo,groups)
        info_serv = InfoService()
        res = info_serv.add_info(name,sex,popo,groups)
        msg='添加成功！'
        data = {'groups':info_serv.get_groups(),'server_msg':msg.decode('utf8')}
        return self.respond('addinfo.html',data)
