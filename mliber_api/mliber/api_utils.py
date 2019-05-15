# -*- coding:utf-8 -*-


def find_library(db, library_id):
    """
    :param db:
    :param library_id:
    :return:
    """
    filters = [["id", "=", library_id], ["status", "=", "Active"]]
    library = db.find_one("Library", filters)
    return library


def find_category(db, category_id):
    """
    :param db:
    :param category_id:
    :return:
    """
    filters = [["id", "=", category_id], ["status", "=", "Active"]]
    category = db.find_one("Category", filters)
    return category


def find_asset(db, asset_name, library_id, category_id):
    """
    :param db:
    :param asset_name: <str>
    :param library_id: <int>
    :param category_id: <int>
    :return:
    """
    filters = [["name", "=", asset_name],
               ["library_id", "=", library_id],
               ["category_id", "=", category_id]]
    asset = db.find_one("Asset", filters)
    return asset
