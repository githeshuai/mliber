# -*- coding: utf-8 -*-
import mliber_global
from mliber_api.database_api import Database


class DatabaseCombined(object):
    def __init__(self, database=None):
        """
        built in
        :param database: <str> custom配置中的database名
        """
        self.__database = database

    @property
    def database(self):
        if self.__database:
            return self.__database
        return mliber_global.app().value("mliber_database")

    @property
    def db(self):
        """
        数据库操作对象
        :param self:
        :return:
        """
        return Database(self.database)

    def create_category(self, name, parent_id, relative_path, library_id, user_id):
        """
        创建类型
        :return:
        """
        category = self.db.create("Category", {"name": name, "parent_id": parent_id, "path": relative_path,
                                               "created_by": user_id, "library_id": library_id})
        return category

    def add_tag_of_asset(self, asset, tag_id):
        """
        :return:
        """
        tag_ids = [tag.id for tag in asset.tags if tag.status == "Active"]
        if tag_id in tag_ids:
            return
        tag_ids.append(tag_id)
        db = self.db
        tags = self.db.find("Tag", [["id", "in", tag_ids]])
        db.update("Asset", asset.id, {"tags": tags})
        db.close()


if __name__ == "__main__":
    print DatabaseCombined("default").db
