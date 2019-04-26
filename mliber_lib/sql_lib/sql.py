# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()


class Sql(object):
    def __init__(self):
        """
        init builtin ...
        """
        self.type = None
        self.__sql_engine = None

    def get_engine_str(self):
        """
        对不同的数据库，engine str方法不一样,继承时需要重写
        :return:
        """
        return None

    def make_engine(self):
        """
        make engine
        :return:
        """
        engine_str = self.get_engine_str()
        engine = create_engine(engine_str, encoding='utf8', convert_unicode=True)
        return engine

    def connect(self):
        """
        创建表格
        :return:
        """
        self.__sql_engine = self.make_engine()
        Base.metadata.create_all(self.__sql_engine)

    def delete_all_table(self):
        """
        :return:
        """
        Base.metadata.drop_all(self.__sql_engine)

    def make_session(self):
        """
        make session
        :return:
        """
        db_session = sessionmaker(self.__sql_engine)
        session = db_session()
        return session
