#!/usr/bin/env python
# encoding: utf-8
from mytor.sa import Engine
from sqlalchemy.engine.strategies import DefaultEngineStrategy


class TornadoStrategy(DefaultEngineStrategy):
    name = "tornado"
    engine_cls = Engine


_STRATEGY = TornadoStrategy()