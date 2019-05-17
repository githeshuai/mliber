# -*- coding:utf-8 -*-
import os
from mliber_conf import mliber_config, templates
from mliber_parse.liber_object_type_parser import LiberObjectType


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


def add_tag_of_asset(db, asset, tag_names):
    """
    :return:
    """
    tag_ids = list()
    for tag_name in tag_names:
        tag = db.find_one("Tag", [["name", "=", tag_name]])
        if not tag:
            tag = db.create("Tag", {"name": tag_name})
        tag_ids.append(tag.id)
    tag_ids = list(set(tag_ids))
    tags = db.find("Tag", [["id", "in", tag_ids]])
    db.update("Asset", asset.id, {"tags": tags})


def get_asset_relative_dir(category, asset_name):
    """
    通过library, category asset name 获取asset dir相对路径
    :param category: <Category>
    :param asset_name: <str>
    :return: 
    """
    asset_dir = os.path.join(category.path, asset_name).replace("\\", "/")
    return asset_dir
    

def get_asset_abs_dir(library, category, asset_name):
    """
    通过library, category asset name 获取asset dir
    :param library: <Library>
    :param category: <Category>
    :param asset_name: <str>
    :return: 
    """
    relative_dir = get_asset_relative_dir(category, asset_name)
    abs_dir = relative_dir.format(root=library.root_path())
    return abs_dir


def get_thumbnail_pattern(asset_dir, asset_name):
    """
    :param asset_dir: <str>
    :param asset_name: <str>
    :return: 
    """
    pattern = templates.THUMBNAIL_PATH.format(asset_dir=asset_dir, asset_name=asset_name)
    return pattern


def get_texture_dir(asset_dir):
    """
    :param asset_dir: <str>
    :return:
    """
    texture_dir = templates.TEXTURE_DIR.format(asset_dir=asset_dir)
    return texture_dir


def get_liber_object_relative_path(asset_relative_dir, liber_object_type, asset_name):
    """
    获取liber object相对路径
    :param asset_relative_dir:
    :param liber_object_type:
    :param asset_name:
    :return:
    """
    ext = LiberObjectType(liber_object_type).ext
    relative_path = templates.LIBER_OBJECT_PATH.format(asset_dir=asset_relative_dir,
                                                       liber_object_type=liber_object_type,
                                                       asset_name=asset_name, ext=ext)
    return relative_path


def get_liber_object_abs_path(library, asset_relative_dir, liber_object_type, asset_name):
    """
    获取liber object绝对路径
    :param library: <Library>
    :param asset_relative_dir: <str>
    :param liber_object_type: <str>
    :param asset_name: <str>
    :return:
    """
    relative_path = get_liber_object_relative_path(asset_relative_dir, liber_object_type, asset_name)
    abs_path = relative_path.format(root=library.root_path())
    return abs_path




