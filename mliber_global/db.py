# -*- coding:utf-8 -*-
import mliber_global
from mliber_api.database_api import Database
from contextlib import contextmanager


@contextmanager
def db(database=None):
    """
    获取db操作对象
    :return:
    """
    if not database:
        database = mliber_global.app().value("mliber_database")
    db_instance = Database(database)
    try:
        yield db_instance
    except:
        db_instance.session.rollback()
