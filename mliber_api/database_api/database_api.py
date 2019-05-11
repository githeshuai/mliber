# -*- coding:utf-8 -*-
from contextlib import contextmanager
from sqlalchemy.sql import and_, or_  # do not delete
from mliber_libs.sql_libs.database_factory import DataBaseFactory
from mliber_tables.tables import User, Library, Category, Asset, Tag, LiberObject


ENTITY_MAPPING = {"User": User,
                  "Library": Library,
                  "Category": Category,
                  "Asset": Asset,
                  "Tag": Tag,
                  "LiberObject": LiberObject}

RELATION_MAPPING = {"is": "is_",
                    "is_not": "isnot",
                    "=": "in_",
                    "!=": "notin_",
                    "in": "in_",
                    "not_in": "notin_",
                    "like": "like",
                    "not_like": "notlike"}


class Database(object):
    pool = dict()
    database = None

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
        return obj

    def __init__(self, name="default"):
        """
        built in
        """
        if not self.database:
            self.name = name
            self.database = DataBaseFactory(self.name).database()
            self.database.connect()
        self.session = self.database.make_session()

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
            
    @staticmethod
    def __get_logical_operator(filter_operator):
        """
        :param filter_operator:
        :return:
        """
        if filter_operator == "all" or filter_operator == "and":
            return "and"
        elif filter_operator == "any" or filter_operator == "or":
            return "or"
        else:
            raise ValueError("Un support filter type")

    @staticmethod
    def __translate_value(relation, value):
        """
        将value转换成适合表达式的值
        :param relation:
        :param value:
        :return:
        """
        if relation in ["like", "not_like"]:
            return "'%s'" % value
        if relation in ["in", "not_in"] or value is None:
            return value
        return [value]

    def __translate_filters_list(self, entity_type, filter_list):
        """
        将dict转换成表达式
        :param entity_type: <str>
        :param filter_list: [["id", "is", 1]]
        :return:
        """
        if not isinstance(filter_list, list):
            raise ValueError("Filter must be a list")
        expressions = list()
        for filter_ in filter_list:
            path, relation, value = filter_
            express = "%s.%s.%s(%s)" % (entity_type, path, RELATION_MAPPING.get(relation),
                                        self.__translate_value(relation, value))
            expressions.append(express)
        return ",".join(expressions)

    def create(self, entity_type, data):
        """
        创建
        :param entity_type: <str>
        :param data: <dict>
        :return:
        """
        entity = ENTITY_MAPPING.get(entity_type)
        obj = entity(**data)
        self.session.add(obj)
        self.session.commit()
        return obj

    def find(self, entity_type, filters, filter_operator="all"):
        """
        查询
        :param entity_type: <str>
        :param filters: <list> like shotgun api
            [["id", "=", 1]]
        :param filter_operator: <str>  "all" "and" “any” "or"
        :return:
        """
        expression = self.__translate_filters_list(entity_type, filters)
        entity = ENTITY_MAPPING.get(entity_type)
        if expression:
            logical_operator = self.__get_logical_operator(filter_operator)
            exp = "%s_(%s)" % (logical_operator, expression)
            entity_instances = self.session.query(entity).filter(eval(exp)).all()
        else:
            entity_instances = self.session.query(entity).all()
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

    def update(self, entity_type, entity_id, data):
        """
        :param entity_type: <str>
        :param entity_id: <int>
        :param data: <dict>
        :return:
        """
        entity_instance = self.find_one(entity_type, [["id", "=", entity_id]])
        if not entity_instance:
            return
        for key, value in data.iteritems():
            setattr(entity_instance, key, value)
        self.session.commit()
        return entity_instance

    def delete(self, entity_instance):
        """
        删除
        :param entity_instance: instance of entity
        :return:
        """
        self.session.delete(entity_instance)
        self.session.commit()

    def create_admin(self):
        """
        创建管理员账户
        :return:
        """
        admin = self.find_one("User", [["name", "=", "admin"], ["status", "=", "Active"]])
        if admin:
            return
        self.create("User", {"name": "admin",
                             "chinese_name": u"管理员",
                             "user_permission": 1,
                             "library_permission": 1})

    def close(self):
        """
        close session
        :return:
        """
        self.session.close()

    def __del__(self):
        """
        close session
        :return:
        """
        self.close()


if __name__ == "__main__":
    db = Database("default")
    # db.create("Library", {"name": "mayaasset", "type": "MayaAsset", "windows_path": "D:/MayaAsset"})
    # db.create("Library", {"name": "nukeasset1", "type": "NukeAsset", "windows_path": "D:/NukeAsset1"})
    assets = db.find("Asset", [["library_id", "=", 1]])
    for asset in assets:
        for tag in asset.tags:
            print tag.name