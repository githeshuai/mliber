# -*- coding:utf-8 -*-
from mliber_libs.sql_libs.mysql import MySql
from mliber_libs.sql_libs.postgresql import PostgreSql
from mliber_libs.sql_libs.sqlite import Sqlite
from mliber_custom.database import DATABASES


class DataBaseFactory(object):
    def __init__(self, name):
        """
        built in
        :param name: database_api name configuration in the config file
        """
        self.name = name
        if not DATABASES. has_key(self.name):
            raise KeyError("There,s no database_api %s in the custom DATABASES." % self.name)
        self.database_conf_data = DATABASES.get(self.name)
        self.type = self.database_conf_data.get("TYPE")
        self.engine = self.database_conf_data.get("ENGINE")
        self.user = self.database_conf_data.get("USER")
        self.password = self.database_conf_data.get("PASSWORD")
        self.host = self.database_conf_data.get("HOST")
        self.database_name = self.database_conf_data.get("NAME")
        self.database_path = self.database_conf_data.get("PATH")

    def database(self):
        """
        生成database对象，类似于工厂
        :return:
        """
        if self.type == "mysql":
            return MySql(self.engine, self.user, self.password, self.host, self.database_name)
        elif self.type == "postgresql":
            return PostgreSql(self.engine, self.user, self.password, self.host, self.database_name)
        elif self.type == "sqlite":
            return Sqlite(self.engine, self.database_path)
        else:
            raise RuntimeError("%s not supported" % self.type)
