# -*- coding:utf-8 -*-
import os
import logging
import pysnooper
from dayu_path import DayuPath
import mliber_global
from mliber_api.api_utils import find_library, find_category, find_asset, get_asset_relative_dir, \
    add_tag_of_asset, get_thumbnail_pattern
from mliber_libs.os_libs.path import Path
from mliber_libs.python_libs.sequence_converter import Converter
from mliber_conf.element_type import ELEMENT_TYPE
from mliber_conf.templates import ELEMENT_PATH, ELEMENT_SEQUENCE_PATH


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
    # 每次上传只支持同一种格式
    ext_list = _get_ext_from_files(files)
    if len(ext_list) > 1:
        return
    with mliber_global.db(database) as db:
        # 确保library存在
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
        element_type = _get_element_type_from_files(files)
        element_relative_path = _get_element_relative_path(files, asset_relative_dir, asset_name)
        element_abs_path = element_relative_path.format(root=library.root_path())
        _copy_source_files(files, element_abs_path)
        logging.info("[MLIBER] info: Copy files done.")
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


def _get_ext_from_file(source_file):
    """
    获取文件格式名字
    :param source_file:
    :return:
    """
    ext = os.path.splitext(source_file)[-1]
    ext = ext.split(".")[-1]
    return ext


def _get_ext_from_files(source_files):
    """
    获取文件格式
    :param source_files: <list>
    :return:
    """
    ext_list = [os.path.splitext(source_file)[-1] for source_file in source_files]
    ext_list = list(set(ext_list))
    return ext_list


def _get_element_type_from_file(source_file):
    """
    根据文件获取element type
    :param source_file: <str> a file path
    :return:
    """
    ext = _get_ext_from_file(source_file)
    element_type = ext if ext in ELEMENT_TYPE else "source"
    return element_type


def _get_element_type_from_files(source_files):
    """
    :param source_files: <str> a file list
    :return:
    """
    if len(source_files) < 1:
        return
    if len(source_files) == 1:
        source_file = source_files[0]
        return _get_element_type_from_file(source_file)
    else:
        ext_list = [os.path.splitext(source_file)[-1] for source_file in source_files]
        ext_list = list(set(ext_list))
        if len(ext_list) > 1:
            return
        return _get_element_type_from_file(source_files[0])


def _get_element_relative_path(source_files, asset_relative_dir, asset_name):
    """
    获取element的相对路径
    :param source_files:
    :return:
    """
    element_type = _get_element_type_from_files(source_files)
    ext = _get_ext_from_file(source_files[0])
    if len(source_files) == 1:
        element_relative_path = ELEMENT_PATH.format(asset_dir=asset_relative_dir, element_type=element_type,
                                                    asset_name=asset_name, ext=ext)
    else:
        element_relative_path = ELEMENT_SEQUENCE_PATH.format(asset_dir=asset_relative_dir,
                                                             element_type=element_type,
                                                             asset_name=asset_name, ext=ext)
    return element_relative_path


def _copy_source_files(source_files, dst_path):
    """
    拷贝文件
    :param source_files: <list>
    :param dst_path: <str> 目标路径, 或者带####的pattern
    :return:
    """
    if len(source_files) == 1:
        Path(source_files[0]).copy_to(dst_path)
    else:
        # 判断是不是序列
        first_file = source_files[0]
        dayu_object = DayuPath(first_file)
        scan_gen = dayu_object.scan()
        scan_list = list(scan_gen)
        frames = scan_list[0].frames
        if frames:
            for index, frame in frames:
                dst_file = dst_path.replace("####", str(frame).zfill(4))
                src_file = source_files[index]
                Path(src_file).copy_to(dst_file)
        else:
            for index, src_file in source_files:
                dst_file = dst_path.replace("####", str(index).zfill(4))
                Path(src_file).copy_to(dst_file)


if __name__ == "__main__":
    a = DayuPath(r"D:\textures\image\images.jpg").scan()
    print list(a)[0].frames