#!/usr/bin/env python
# encoding: utf-8
from tornado.gen import coroutine
from sqlalchemy.engine import Engine as BaseEngine


# class Engine(BaseEngine):
#     def contextual_connect(self, close_with_result=False, **kwargs):
#         pass


class Engine:
    """Connects a aiopg.Pool and
    sqlalchemy.engine.interfaces.Dialect together to provide a
    source of database connectivity and behavior.
    An Engine object is instantiated publicly using the
    create_engine coroutine.
    """

    def __repr__(self):
        # Mimic on the base class
        return 'AsyncEngine(%r)' % self.url

    def __init__(self, dialect, pool, dsn):
        self._dialect = dialect
        self._pool = pool
        self._dsn = dsn

    @property
    def dialect(self):
        """An dialect for engine."""
        return self._dialect

    @property
    def name(self):
        """A name of the dialect."""
        return self._dialect.name

    @property
    def driver(self):
        """A driver of the dialect."""
        return self._dialect.driver

    @property
    def dsn(self):
        """DSN connection info"""
        return self._dsn

    @property
    def timeout(self):
        return self._pool.timeout

    @property
    def minsize(self):
        return self._pool.minsize

    @property
    def maxsize(self):
        return self._pool.maxsize

    @property
    def size(self):
        return self._pool.size

    @property
    def freesize(self):
        return self._pool.freesize

    def close(self):
        """Close engine.
        Mark all engine connections to be closed on getting back to pool.
        Closed engine doesn't allow to acquire new connections.
        """
        self._pool.close()

    def terminate(self):
        """Terminate engine.
        Terminate engine pool with instantly closing all acquired
        connections also.
        """
        self._pool.terminate()

    @coroutine
    def wait_closed(self):
        """Wait for closing all engine's connections."""
        yield from self._pool.wait_closed()

    @coroutine
    def acquire(self):
        """Get a connection from pool."""
        raw = yield from self._pool.acquire()
        conn = SAConnection(raw, self)
        return conn

    def release(self, conn):
        """Revert back connection to pool."""
        if conn.in_transaction:
            raise InvalidRequestError("Cannot release a connection with "
                                      "not finished transaction")
        raw = conn.connection
        self._pool.release(raw)

    def __enter__(self):
        raise RuntimeError(
            '"yield from" should be used as context manager expression')

    def __exit__(self, *args):
        # This must exist because __enter__ exists, even though that
        # always raises; that's how the with-statement works.
        pass  # pragma: nocover

    def __iter__(self):
        # This is not a coroutine.  It is meant to enable the idiom:
        #
        #     with (yield from engine) as conn:
        #         <block>
        #
        # as an alternative to:
        #
        #     conn = yield from engine.acquire()
        #     try:
        #         <block>
        #     finally:
        #         engine.release(conn)
        conn = yield from self.acquire()
        return _ConnectionContextManager(self, conn)