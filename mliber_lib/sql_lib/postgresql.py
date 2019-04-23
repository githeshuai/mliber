# -*- coding:utf-8 -*-
from mliber_lib.sql_lib.sql import Sql
from mliber_conf.databse_engine_url import ENGINE_URL


class PostgreSql(Sql):
    def __init__(self, engine, user, password, host, database_name):
        """
        :param engine:
        :param user:
        :param password:
        :param host:
        :param database_name:
        """
        super(PostgreSql, self).__init__()
        self.engine = engine
        self.user = user
        self.password = password
        self.host = host
        self.database_name = database_name

    def get_engine_str(self):
        engine_url = ENGINE_URL.get("postgresql")
        engine_str = engine_url.format(engine=self.engine, user=self.user, password=self.password,
                                       host=self.host, database=self.database_name)
        return engine_str
