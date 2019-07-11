# -*- coding: utf-8 -*-
import mliber_global
from mliber_conf import mliber_config
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

    def create_library(self, name, typ, windows_path, linux_path, mac_path, description="", created_by=None):
        """
        创建library
        :param name: <str>
        :param typ: <str>
        :param windows_path: <str>
        :param linux_path: <str>
        :param mac_path: <str>
        :param description: <str>
        :param created_by: <int>
        :return:
        """
        data = {"name": name, "type": typ, "windows_path": windows_path,
                "linux_path": linux_path, "mac_path": mac_path, "description": description}
        if created_by:
            data.update({"created_by": created_by})
        library = self.db.create("Library", data)
        return library

    def create_category(self, name, parent_id, relative_path, library_id, created_by):
        """
        创建类型
        :param name: <str>
        :param parent_id: <int>
        :param relative_path: <str> 相对路径
        :param library_id: <int>
        :param created_by: <int>
        :return:
        """
        db = self.db
        if parent_id is None:
            categories = db.find("Category", [["parent_id", "is", parent_id]])
        else:
            categories = db.find("Category", [["parent_id", "=", parent_id]])
        category_names = [category.name for category in categories]
        if name in category_names:
            category = db.find_one("Category", [["name", "=", name]])
            db.update("Category", category.id, {"status": "Active"})
        else:
            data = {"name": name, "parent_id": parent_id, "path": relative_path, "library_id": library_id}
            if created_by:
                data.update({"created_by": created_by})
            category = self.db.create("Category", data)
        return category

    def create_tag(self, tag_name, colorR=None, colorG=None, colorB=None, created_by=None):
        """
        创建tag
        :param tag_name: <str>
        :param colorR: <int>
        :param colorG: <int>
        :param colorB: <int>
        :param created_by:
        :return:
        """
        db = self.db
        tag = db.find_one("Tag", [["name", "=", tag_name]])
        if not tag:
            colorR = colorR or mliber_config.TAG_COLOR_R
            colorG = colorG or mliber_config.TAG_COLOR_G
            colorB = colorB or mliber_config.TAG_COLOR_B
            data = {"name": tag_name, "colorR": colorR, "colorG": colorG, "colorB": colorB}
            if created_by:
                data.update({"created_by": created_by})
            tag = db.create("Tag", data)
        return tag

    def add_tag_of_asset(self, asset, tag_id):
        """
        :return:
        """
        tag_ids = [tag.id for tag in asset.tags]
        if tag_id in tag_ids:
            return
        tag_ids.append(tag_id)
        db = self.db
        tags = self.db.find("Tag", [["id", "in", tag_ids]])
        db.update("Asset", asset.id, {"tags": tags})
        db.close()

    def tags_of_assets(self, assets):
        """
        获取该library下所有资产的tag
        :param assets: <list> Asset instance list
        :return:
        """
        tags = list()
        asset_tags = list()
        for asset in assets:
            asset_tags.extend(asset.tags)
        if asset_tags:
            tag_names = [tag.name for tag in asset_tags]
            tag_names = list(set(tag_names))
            tags = self.db.find("Tag", [["name", "in", tag_names]])
        return tags


if __name__ == "__main__":
    db = DatabaseCombined("sqlite")
    # parent_id, relative_path, library_id, created_by
    db.create_category("test", None, "{root}/test", 2, 1)
