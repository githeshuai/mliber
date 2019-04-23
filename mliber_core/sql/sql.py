# -*- coding:utf-8 -*-
from datetime import datetime
from contextlib import contextmanager



from mliber_lib.sql_lib.database_factory import DataBaseFactory
from mliber_tables.tables import User, Library, Category, Asset, Tag


class Sql(object):
    pool = dict()
    __has_init = False

    def __new__(cls, name="default"):
        """
        singleton
        :param name:
        :return:
        """
        obj = cls.pool.get(name, None)
        if not obj:
            obj = object.__new__(cls)
            cls.pool[name] = obj
            obj.name = name
        return obj

    def __init__(self):
        """
        built in
        """
        if not self.__has_init:
            database = DataBaseFactory(self.name).database()
            database.connect()
            self.session = database.make_session()
            self.__has_init = True

    @contextmanager
    def get_session(self):
        try:
            yield self.session
        except RuntimeError as e:
            print str(e)
            self.session.rollback()
        finally:
            self.session.close()

    def create_user(self, name, chinese_name, created_by, password="123456", user_permission=False,
                    library_permission=False, category_permission=False, asset_permission=True, tag_permission=True,
                    status="Active", description=""):
        now = datetime.now()
        with self.get_session() as session:
            user = User(name=name, chinese_name=chinese_name, created_at=now, created_by=created_by, password=password,
                        user_permission=user_permission, library_permission=library_permission,
                        category_permission=category_permission, asset_permission=asset_permission,
                        tag_permission=tag_permission, status=status, description=description)
            session.add(user)
            session.commit()


if __name__ == "__main__":
    import datetime
    now = datetime.datetime.now()
    Sql().create_user("lisi", "李四", 1, )
