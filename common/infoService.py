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

    def test_info(self):
        return self.db.db_exec("call list_fellow('')");
