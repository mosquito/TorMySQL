#!/usr/bin/env python
# encoding: utf-8
from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql


class Dialect(MySQLDialect_pymysql):
    implicit_returning = True