# encoding: utf-8
import re
from mytor.sa.engine import Engine
from mytor.sa.strategy import _STRATEGY
from sqlalchemy.dialects import registry
from tornado.ioloop import IOLoop
from ..pool import ConnectionPool
from .engine import Engine
from .dialect import Dialect

_TIMEOUT = 7200
_DIALECT = Dialect()
_MODULE = 'mysql'

_URL_RE = re.compile(
    '^(?P<scheme>\w+):\/\/'
    '((((?P<user>[^:^@]+))?'
    '((\:(?P<password>[^@]+)?))?\@)?'
    '(?P<host>[^\/^:]+)'
    '(\:(?P<port>\d+))?)?'
    '(((?P<path>\/[^\?]*)'
    '(\?(?P<query>[^\#]+))?'
    '(\#(?P<anchor>.*))?))?$'
)


def create_engine(db_url, minsize=10, maxsize=10, *args, **kwargs):
    if _MODULE not in registry.impls:
        registry.register(_MODULE, 'mytor.sa.dialect', 'Dialect')

    dialect = kwargs.pop('_dialect', _DIALECT)
    timeout = kwargs.pop('timeout', _TIMEOUT)
    io_loop = kwargs.pop('loop', None)

    if io_loop is None:
        io_loop = IOLoop.current()

    matcher = _URL_RE.match(db_url)
    if matcher is None:
        raise ValueError("Invalid DB URL: %r" % db_url)

    url_parts = matcher.groupdict()
    kwargs.update(dict(
        host=url_parts['host'],
        user=url_parts['user'],
        password=url_parts['password'],
        database=url_parts['path'].strip('/'),
        port=int(url_parts.get('port') or '3306'),
        io_loop=io_loop,
        idle_seconds=timeout,
        max_connections=maxsize,
    ))

    return Engine(
        dialect,
        ConnectionPool(*args, **kwargs),
        db_url
    )

