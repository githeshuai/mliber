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


class Asset(object):
    def __init__(self, database, library_id, category_id, asset_name, files,
                 overwrite=True, description="", tags=list(), thumbnail_files=list(), created_by=None, **kwargs):
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
        self._database = database
        self._library_id = library_id
        self._category_id = category_id
        self._asset_name = asset_name
        self._files = files
        self._overwrite = overwrite
        self._description = description
        self._tags = tags
        self._thumbnail_files = thumbnail_files
        self._created_by = created_by
        self._start = 1
        self._end = 1

    @staticmethod
    def _get_ext_from_file(source_file):
        """
        获取文件格式名字
        :param source_file:
        :return:
        """
        ext = os.path.splitext(source_file)[-1]
        ext = ext.split(".")[-1]
        return ext

    @staticmethod
    def _get_ext_from_files(source_files):
        """
        获取文件格式
        :param source_files: <list>
        :return:
        """
        ext_list = [os.path.splitext(source_file)[-1] for source_file in source_files]
        ext_list = list(set(ext_list))
        return ext_list

    def _get_element_type_from_file(self, source_file):
        """
        根据文件获取element type
        :param source_file: <str> a file path
        :return:
        """
        ext = self._get_ext_from_file(source_file)
        element_type = ext if ext in ELEMENT_TYPE else "source"
        return element_type

    def _get_element_type_from_files(self, source_files):
        """
        :param source_files: <str> a file list
        :return:
        """
        if len(source_files) < 1:
            return
        if len(source_files) == 1:
            source_file = source_files[0]
            return self._get_element_type_from_file(source_file)
        else:
            ext_list = self._get_ext_from_files(source_files)
            if len(ext_list) > 1:
                return
            return self._get_element_type_from_file(source_files[0])

    def _get_element_relative_path(self, source_files, asset_relative_dir, asset_name):
        """
        获取element的相对路径
        :param source_files:
        :return:
        """
        element_type = self._get_element_type_from_files(source_files)
        ext = self._get_ext_from_file(source_files[0])
        if len(source_files) == 1:
            element_relative_path = ELEMENT_PATH.format(asset_dir=asset_relative_dir, element_type=element_type,
                                                        asset_name=asset_name, ext=ext)
        else:
            element_relative_path = ELEMENT_SEQUENCE_PATH.format(asset_dir=asset_relative_dir,
                                                                 element_type=element_type,
                                                                 asset_name=asset_name, ext=ext)
        return element_relative_path

    def _copy_source_files(self, source_files, dst_path):
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
            missing = scan_list[0].missing
            if frames:
                self._start = frames[0]
                self._end = frames[-1]
                if missing:
                    logging.warning(u"有丢失的帧：%s" % ",".join(missing))
                for index, frame in enumerate(frames):
                    dst_file = dst_path.replace("####", str(frame).zfill(4))
                    src_file = source_files[index]
                    if index >= len(source_files)-1:
                        break
                    Path(src_file).copy_to(dst_file)
            else:
                for index, src_file in enumerate(source_files):
                    dst_file = dst_path.replace("####", str(index).zfill(4))
                    Path(src_file).copy_to(dst_file)

    def _create_element(self, db, element_type, element_relative_path):
        """
        创建element
        :param db:
        :param element_type: <str>
        :param element_relative_path: <str>
        :return:
        """
        element_name = "%s_%s" % (self._asset_name, element_type)
        element_data = {"name": element_name, "type": element_type,
                        "path": element_relative_path, "status": "Active",
                        "start": self._start, "end": self._end}
        if self._created_by is not None:
            element_data.update({"created_by": self._created_by})
        element = db.create("Element", element_data)
        return element

    def _create_asset(self, db, asset_relative_dir, elements, asset_info):
        """
        :param db:
        :param asset_relative_dir: <str>
        :param elements: <list>
        :param asset_info: <Asset>
        :return:
        """
        asset_data = {"name": self._asset_name, "path": asset_relative_dir, "status": "Active",
                      "library_id": self._library_id, "category_id": self._category_id,
                      "description": self._description, "elements": elements}
        if self._created_by is not None:
            asset_data.update({"created_by": self._created_by})
        if not asset_info:
            asset = db.create("Asset", asset_data)
        else:
            asset = db.update("Asset", asset_info.id, asset_data)
        return asset

    @pysnooper.snoop()
    def create(self):
        # 每次上传只支持同一种格式
        ext_list = self._get_ext_from_files(self._files)
        if len(ext_list) > 1:
            return
        with mliber_global.db(self._database) as db:
            # 确保library存在
            library = find_library(db, self._library_id)
            if not library:
                logging.error("[MLIBER] error: library not exist.")
                return
            # 确保category存在
            category = find_category(db, self._category_id)
            if not category:
                logging.error("[MLIBER] error: Category not exist.")
                return
            # 判断资产是否存在
            asset_info = find_asset(db, self._asset_name, self._library_id, self._category_id)
            if asset_info and not self._overwrite:  # 如果资产存在，并且不允许覆盖
                logging.error("[MLIBER] error: Asset already exist.")
                return
            asset_relative_dir = get_asset_relative_dir(category, self._asset_name)
            asset_abs_dir = asset_relative_dir.format(root=library.root_path())
            # 转换缩略图
            thumbnail_pattern = get_thumbnail_pattern(asset_abs_dir, self._asset_name)
            Converter().convert(self._thumbnail_files, thumbnail_pattern)
            logging.info("[MLIBER] info: Convert thumbnail done.")
            # 拷贝文件
            element_type = self._get_element_type_from_files(self._files)
            element_relative_path = self._get_element_relative_path(self._files, asset_relative_dir, self._asset_name)
            element_abs_path = element_relative_path.format(root=library.root_path())
            self._copy_source_files(self._files, element_abs_path)
            logging.info("[MLIBER] info: Copy files done.")
            # 创建element
            element = self._create_element(db, element_type, element_relative_path)
            logging.info("[MLIBER] info: Create element done.")
            # 创建资产
            asset = self._create_asset(db, asset_relative_dir, [element], asset_info)
            logging.info("[MLIBER] info: Create Asset done.")
            if self._tags:
                add_tag_of_asset(db, asset, self._tags)
                logging.info("[MLIBER] info: Assign Tag done.")
            return asset
