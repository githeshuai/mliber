# -*- coding:utf-8 -*-
from contextlib import contextmanager
from mliber_lib.sql_lib.database_factory import DataBaseFactory
from mliber_tables.tables import User, Library, Category, Asset, Tag


@contextmanager
def get_session(name):
    try:
        database = DataBaseFactory(name).database()
        database.connect()
        session = database.make_session()
        yield session
    except RuntimeError as e:
        session.rollback()
        print str(e)
    finally:
        session.close()


class Sql(object):
    pool = dict()
    __has_init = False

    def __new__(cls, name="default"):
        obj = cls.pool.get(name, None)
        if not obj:
            obj = object.__new__(cls)
            cls.pool[name] = obj
            obj.name = name
        return obj

    def __init__(self):
        pass

    def test(self):
        with get_session(self.name) as session:
            print session


if __name__ == "__main__":
    sql = Sql()
    sql.test()
