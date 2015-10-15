mytor
=====

.. image:: https://travis-ci.org/mosquito/mytor.svg
    :target: https://travis-ci.org/mosquito/mytor

Tornado asynchronous MySQL Driver.

This if fork of TorMySQL_.

.. _TorMySQL: https://github.com/snower/TorMySQL

About
=====

mytor - presents a Tornado Future-based API and greenlet for
non-blocking access to MySQL.

Installation
============

::

    pip install mytor

Examples
========

::

    import mytor
    from tornado.ioloop import IOLoop
    from tornado.gen import coroutine


    pool = mytor.ConnectionPool(
        max_connections = 20,       #max open connections
        idle_seconds = 7200,        #conntion idle timeout time, 0 is not timeout
        host = "127.0.0.1",
        user = "root",
        passwd = "secret",
        db = "test",
        charset = "utf8"
    )


    @coroutine
    def test():
        with (yield pool.Connection()) as conn:
            with conn.cursor() as cursor:
                yield cursor.execute("SELECT * FROM test")
                datas = cursor.fetchall()

        print datas
        yield pool.close()

    IOLoop.current().run_sync(test)
