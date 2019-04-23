# -*- coding:utf-8 -*-
from mliber_lib.sql_lib.sql import Sql
from mliber_conf.databse_engine_url import ENGINE_URL


class Sqlite(Sql):
    def __init__(self, engine, path):
        """
        :param engine:
        :param path: .db path
        """
        super(Sqlite, self).__init__()
        self.engine = engine
        self.path = path

    def get_engine_str(self):
        engine_url = ENGINE_URL.get("sqlite")
        engine_str = engine_url.format(engine=self.engine, path=self.path)
        return engine_str
