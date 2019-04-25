# -*- coding:utf-8 -*-
from contextlib import contextmanager
from sqlalchemy.sql import and_, or_
from mliber_lib.sql_lib.database_factory import DataBaseFactory
from mliber_tables.tables import User, Library, Category, Asset, Tag


ENTITY_MAPPING = {"User": User, "Library": Library, "Category": Category,
                  "Asset": Asset, "Tag": Tag}


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
        """
        get session
        :return:
        """
        try:
            yield self.session
        except RuntimeError as e:
            print str(e)
            self.session.rollback()
        finally:
            self.session.close()

    def create(self, entity_type, **data):
        """
        创建
        :param entity_type: <str>
        :param data: name="apple", library_id=1
        :return:
        """
        with self.get_session() as session:
            entity = ENTITY_MAPPING.get(entity_type)
            obj = entity(**data)
            session.add(obj)
            session.commit()

    def find(self, entity_type, filters, filter_operator="all"):
        """
        查询
        :param entity_type: <str>
        :param filters: <list> [Asset.id=1， Asset.name.like("%pea")]
        :param filter_operator: <str>  "all" "and" “any” "or"
        :return:
        """
        entity = ENTITY_MAPPING.get(entity_type)
        if filter_operator in ["all", "and"]:
            entity_instances = self.session.query(entity).filter(and_(*filters)).all()
        elif filter_operator in ["any", "or"]:
            entity_instances = self.session.query(entity).filter(or_(*filters)).all()
        else:
            raise RuntimeError("%s filter_operator not supported" % filter_operator)
        return entity_instances

    def find_one(self, entity_type, filters, filter_operator="all"):
        """
        :param entity_type:
        :param filters: <list> [Asset.id=1， Asset.name.like("%pea")]
        :param filter_operator: <str>  "all" "and" “any” "or"
        :return:
        """
        entity_instances = self.find(entity_type, filters, filter_operator)
        return entity_instances[0] if entity_instances else None

    def update(self, entity_instance, **kwargs):
        """
        Sql().update(asset, user_id=1, name="banana")
        :param entity_instance: instance of entity
        :return:
        """
        with self.get_session() as session:
            for key, value in kwargs.iteritems():
                setattr(entity_instance, key, value)
                session.commit()

    def delete(self, entity_instance):
        """
        删除
        :param entity_instance: instance of entity
        :return:
        """
        with self.get_session() as session:
            session.delete(entity_instance)
            session.commit()


if __name__ == "__main__":
    print Sql().find_one("Asset", [Asset.id == 2]).tags
