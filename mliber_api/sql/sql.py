# -*- coding:utf-8 -*-
from contextlib import contextmanager
from sqlalchemy.sql import and_, or_
from mliber_lib.sql_lib.database_factory import DataBaseFactory
from mliber_tables.tables import User, Library, Category, Asset, Tag


ENTITY_MAPPING = {"User": User,
                  "Library": Library,
                  "Category": Category,
                  "Asset": Asset, "Tag": Tag}

RELATION_MAPPING = {"is": "is_",
                    "is_not": "isnot",
                    "=": "in_",
                    "!=": "notin_",
                    "in": "in_",
                    "not_in": "notin_",
                    "like": "like",
                    "not_like": "notlike"}


class Sql(object):
    pool = dict()
    __has_init = False

    def __new__(cls, name):
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

    def __init__(self, name):
        """
        built in
        """
        if not self.__has_init:
            self.name = name
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

    def create(self, entity_type, **data):
        """
        创建
        :param entity_type: <str>
        :param data: name="apple", library_id=1
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
        注意： 中文的查询用relation用in，不要用=， =会报错，很懵逼
        :param entity_type: <str>
        :param filters: <list> like shotgun api
            [["id", "is", 1]]
        :param filter_operator: <str>  "all" "and" “any” "or"
        :return:
        """
        expression = self.__translate_filters_list(entity_type, filters)
        logical_operator = self.__get_logical_operator(filter_operator)
        entity = ENTITY_MAPPING.get(entity_type)
        if expression:
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
        self.session.delete(entity_instance)
        self.session.commit()


if __name__ == "__main__":
    sql = Sql("default")
    parent = sql.create("Category", name=u"植物")
    trees = sql.create("Category", name=u"树木", parent_id=parent.id)
    sql.create("Category", name=u"蔬菜", parent_id=parent.id)
    sql.create("Category", name="桂花树", parent_id=trees.id)
    # print sql.session.query(Category).filter(Category.parent_id.in_([None])).all()
    # sql = Sql()
    # categories = sql.find("Category", [["name", "like", u"%物"], ["id", "in", [3]]], "any")
    # for category in categories:
    #     print category.name
