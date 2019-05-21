# -*- coding:utf-8 -*-
import os
import logging
import pysnooper
import mliber_global
from mliber_api.api_utils import find_library, find_category, find_asset, get_asset_relative_dir, \
    add_tag_of_asset, get_thumbnail_pattern
from mliber_libs.os_libs.path import Path
from mliber_libs.python_libs.sequence_converter import Converter
from mliber_conf.element_type import ELEMENT_TYPE
from mliber_conf.templates import ELEMENT_PATH


@pysnooper.snoop()
def create(database, library_id, category_id, asset_name, files,
           overwrite=True, description="", tags=list(), thumbnail_files=list(), created_by=None):
    """
    从外部创建资产
    :param database: <str> custom配置文件中的数据库名字
    :param library_id: <int>
    :param category_id: <int>
    :param asset_name: <str>
    :param files: <list> 需要上传的文件
    :param overwrite: <bool> 如果资产存在是否覆盖
    :param description: <str> 描述
    :param tags: <list> 标签列表
    :param thumbnail_files: <list> 缩略图文件
    :param created_by: <int> 用户id
    :return:
    """
    with mliber_global.db(database) as db:
        library = find_library(db, library_id)
        if not library:
            logging.error("[MLIBER] error: library not exist.")
            return
        # 确保category存在
        category = find_category(db, category_id)
        if not category:
            logging.error("[MLIBER] error: Category not exist.")
            return
        # 判断资产是否存在
        asset_info = find_asset(db, asset_name, library_id, category_id)
        if asset_info and not overwrite:  # 如果资产存在，并且不允许覆盖
            logging.error("[MLIBER] error: Asset already exist.")
            return
        asset_relative_dir = get_asset_relative_dir(category, asset_name)
        asset_abs_dir = asset_relative_dir.format(root=library.root_path())
        # 转换缩略图
        thumbnail_pattern = get_thumbnail_pattern(asset_abs_dir, asset_name)
        Converter().convert(thumbnail_files, thumbnail_pattern)
        logging.info("[MLIBER] info: Convert thumbnail done.")
        # 拷贝文件
        if len(files) == 1:
            source_file = files[0]
            ext = os.path.splitext(source_file)[-1]
            element_type = _get_element_type_from_file(source_file)
            element_relative_path = ELEMENT_PATH.format(asset_dir=asset_relative_dir, element_type=element_type,
                                                        asset_name=asset_name, ext=ext)
            element_abs_path = element_relative_path.format(root=library.root_path())
            Path(source_file).copy_to(element_abs_path)
            # 创建element
            element_name = "%s_%s" % (asset_name, element_type)
            element_data = {"name": element_name, "type": element_type,
                            "path": element_relative_path, "status": "Active"}
            if created_by is not None:
                element_data.update({"created_by": created_by})
            element = db.create("Element", element_data)
            logging.info("[MLIBER] info: Create element done.")
            # 创建资产
            asset_data = {"name": asset_name, "path": asset_relative_dir, "status": "Active",
                          "library_id": library_id, "category_id": category_id, "description": description,
                          "elements": [element]}
            if created_by is not None:
                asset_data.update({"created_by": created_by})
            if not asset_info:
                asset = db.create("Asset", asset_data)
            else:
                asset = db.update("Asset", asset_info.id, asset_data)
            logging.info("[MLIBER] info: Create Asset done.")
            if tags:
                add_tag_of_asset(db, asset, tags)
                logging.info("[MLIBER] info: Assign Tag done.")
            if not asset_info:
                return asset


def _get_element_type_from_file(source_file):
    """
    :param source_file: <str> a file path
    :return:
    """
    ext = os.path.splitext(source_file)[-1]
    ext = ext.split(".")[-1]
    element_type = ext if ext in ELEMENT_TYPE else "source"
    return element_type
