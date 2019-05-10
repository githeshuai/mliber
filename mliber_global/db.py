# -*- coding:utf-8 -*-
import mliber_global
from mliber_api.database_api import Database
from contextlib import contextmanager


@contextmanager
def db():
    """
    获取db操作对象
    :return:
    """
    database = mliber_global.app().value("mliber_database")
    db = Database(database)
    try:
        yield db
    except:
        db.session.rollback()
    finally:
        db.session.close()
