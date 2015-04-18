#!/usr/bin/env python
# coding=utf-8
import MySQLdb

from config import config

class DB(object):

    def __init__(self):
        self._db = MySQLdb.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            passwd=config.DB_PASS,
            db=config.DB_NAME,
            port=config.DB_PORT,
            charset=config.DB_CHARSET,
            unix_socket='/tmp/mysql.sock'
            )
        self._db.autocommit(True)

    def db_exec(self,sql,params=()):
        c=self._db.cursor(MySQLdb.cursors.DictCursor)
        try:
            c.execute(sql,params)
            return c.fetchall()
        finally:
            c.close()

    def callproc(self,func,params=()):
        c=self._db.cursor()
        try:
            c.callproc(func,params)
            return c.fetchone()
        finally:
            c.close()

