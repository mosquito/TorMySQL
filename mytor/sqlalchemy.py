# encoding: utf-8
from sqlalchemy.dialects import registry
from sqlalchemy.engine.strategies import DefaultEngineStrategy
from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql
from sqlalchemy.engine.base import Engine as BaseEngine


class Engine(BaseEngine):
    pass


class TornadoStrategy(DefaultEngineStrategy):
    name = "tornado"
    engine_cls = Engine

strategy = TornadoStrategy()


class Dialect(MySQLDialect_pymysql):
    pass


def create_engine(*args, **kwargs):
    registry.register('mysql.mytor', 'mytor.sqlalchemy', 'Dialect')
    return strategy.create(*args, **kwargs)
