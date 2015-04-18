#!/usr/bin/env python
# coding=utf-8
import logging
from MySQLdb import escape_string

import db

class InfoService(object):

    def __init__(self):
        if not globals().get('db_ins'):
            global db_ins
            db_ins = db.DB()
        self.db = db_ins

    def show_info(self,name=''):
        sql = "call list_fellow('%s');" % escape_string(name)
        return self.db.db_exec(sql)
    
    def get_groups(self):
        sql = "call show_groups();"
        return self.db.db_exec(sql)
    
    def add_info(self,name,sex,popo,group):
        sql = "call add_info('%s',%d,'%s',%d)" % (escape_string(name),sex,escape_string(popo),group)
        return self.db.db_exec(sql)
