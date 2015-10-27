# encoding: utf-8
from sqlalchemy.dialects import registry
from sqlalchemy.engine.strategies import DefaultEngineStrategy
from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql
from sqlalchemy.engine.base import Engine as BaseEngine


class Engine(BaseEngine):
    pass


class Dialect(MySQLDialect_pymysql):
    pass


class TornadoStrategy(DefaultEngineStrategy):
    name = "tornado"
    engine_cls = Engine

_STRATEGY = TornadoStrategy()


def create_engine(*args, **kwargs):
    module_name = 'mysql.mytor'

    if module_name not in registry.impls:
        registry.register(module_name, 'mytor.sqlalchemy', 'Dialect')

    return _STRATEGY.create(*args, **kwargs)
