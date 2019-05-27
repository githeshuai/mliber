# -*- coding:utf-8 -*-
import logging
import pysnooper
from mliber_api.api_utils import find_library, find_category, find_asset, \
    get_asset_relative_dir, get_thumbnail_pattern, get_element_relative_path, add_tag_of_asset
import mliber_global
from mliber_libs.dcc_libs.dcc import Dcc
from mliber_libs.python_libs.sequence_converter import Converter
from mliber_libs.os_libs.path import Path
from mliber_parse.element_type_parser import ElementType
from mliber_utils import load_hook


class AssetMaker(object):
    def __init__(self, database_name, library_id, category_id, asset_name, objects, types, start=1, end=1,
                 thumbnail_files=list(), tag_names=list(), description="", overwrite=True, created_by=None):
        """
        maya资产创建
        :param database_name: custom配置中的database名字
        :param library_id: <int> library id
        :param category_id: <int> category id
        :param asset_name: <str> 资产名字
        :param objects: <list> 需要导出的物体
        :param types: <list> 需要导出的类型列表
        :param thumbnail_files: <list> 缩略图路径，
        :param start: <int> 起始帧
        :param end: <int> 结束帧
        :param tag_names: <list> 标签名字
        :param description: <str> 描述
        :param overwrite: <bool> 如果资产存在,是否覆盖
        :param created_by: <int> 创建者ID
        :return:
        """
        self.database = database_name
        self.library_id = library_id
        self.category_id = category_id
        self.asset_name = asset_name
        self.objects = objects
        self.types = types
        self.start = start
        self.end = end
        self.thumbnail_files = thumbnail_files
        self.tag_names = tag_names
        self.description = description
        self.overwrite = overwrite
        self.created_by = created_by
        #
        self.db = None  # database api操作对象
        self.library = None  # Library 实体
        self.category = None  # Category 实体
        self.asset_info = None  # Asset实体

    @property
    def asset_relative_dir(self):
        """
        资产相对路径
        :return:
        """
        asset_relative_dir = get_asset_relative_dir(self.category, self.asset_name)
        return asset_relative_dir

    @property
    def asset_abs_dir(self):
        """
        资产绝对路径
        :return:
        """
        asset_abs_dir = self.asset_relative_dir.format(root=self.library.root_path())
        return asset_abs_dir

    def convert_thumbnail(self):
        """
        转换缩略图
        :return:
        """
        thumbnail_pattern = get_thumbnail_pattern(self.asset_abs_dir, self.asset_name)
        Converter().convert(self.thumbnail_files, thumbnail_pattern)
        logging.info("[MLIBER] info: Convert thumbnail done.")

    def _create_element(self, db, element_type, element_relative_path, software="", plugin=""):
        """
        创建element
        :param db:
        :param element_type: <str>
        :param element_relative_path: <str>
        :return:
        """
        element_name = "%s_%s" % (self.asset_name, element_type)
        element_data = {"name": element_name, "type": element_type, "path": element_relative_path, "status": "Active",
                        "start": self.start, "end": self.end, "software": software, "plugin": plugin}
        if self.created_by is not None:
            element_data.update({"created_by": self.created_by})
        element = db.create("Element", element_data)
        return element

    def pre_create_elements(self):
        """
        在创建elements之前需要执行的操作，比如maya，需要先导出贴图
        :return:
        """
        return True

    def post_create_elements(self):
        """
        创建elements之后需要执行的操作，比如maya，需要将贴图路径还原
        :return:
        """
        return True

    def create_elements(self):
        """
        创建elements
        :return:
        """
        elements = []
        for element_type in self.types:
            # 相对路径，保存于数据库
            element_relative_path = get_element_relative_path(self.asset_relative_dir, element_type, self.asset_name)
            element_abs_path = element_relative_path.format(root=self.library.root_path())  # 绝对路径，导出在磁盘上的路径
            action = ElementType(element_type).export_action_of_engine(Dcc.engine())  # 读取配置文件中，有哪些action
            if not action:
                logging.warning("[MLIBER] warning: No export action configured of %s" % element_type)
                continue
            try:
                hook = load_hook(action.hook)
                hook_instance = hook.Hook(element_abs_path, self.objects, self.start, self.end, self.asset_name)
                exported_path = hook_instance.main()
            except Exception as e:
                logging.error("[MLIBER] error: %s" % str(e))
                continue
            if not exported_path:
                continue
            plugin = hook_instance.plugin_version()
            relative_dir = Path(element_relative_path).parent()
            element_relative_path = Path(relative_dir).join(Path(exported_path).basename())  # element relative path
            element = self._create_element(self.db, element_type, element_relative_path, Dcc().software(), plugin)
            elements.append(element)
            logging.info("[MLIBER] info: Export %s done." % element_type)
        return elements

    def create_asset(self, elements):
        """
        创建资产
        :param elements: <list> [Element, .....]
        :return:
        """
        # create asset
        asset_data = {"name": self.asset_name, "path": self.asset_relative_dir, "status": "Active",
                      "library_id": self.library_id, "category_id": self.category_id,
                      "description": self.description, "elements": elements}
        if self.created_by is not None:
            asset_data.update({"created_by": self.created_by})
        if not self.asset_info:
            asset = self.db.create("Asset", asset_data)
        else:
            asset = self.db.update("Asset", self.asset_info.id, asset_data)
        logging.info("[MLIBER] info: Create Asset done.")
        # add tag
        if self.tag_names:
            add_tag_of_asset(self.db, asset, self.tag_names)
            logging.info("[MLIBER] info: Assign Tag done.")
        return asset

    def _pre_make(self, db):
        """
        检查
        :return: <list> [Library, Category, Asset]
        """
        library = find_library(db, self.library_id)
        if not library:
            logging.error("[MLIBER] error: library not exist.")
            return []
        # 确保category存在
        category = find_category(db, self.category_id)
        if not category:
            logging.error("[MLIBER] error: Category not exist.")
            return []
        # 判断资产是否存在
        asset_info = find_asset(db, self.asset_name, self.library_id, self.category_id)
        return [library, category, asset_info]

    def preflight(self):
        """
        在创建之前检查
        :return:
        """
        return True

    @pysnooper.snoop()
    def make(self):
        if not self.preflight():
            return
        with mliber_global.db(self.database) as db:
            self.db = db
            result = self._pre_make(db)
            if not result:
                return
            self.library, self.category, self.asset_info = result
            if self.asset_info and not self.overwrite:  # 如果资产存在，并且不允许覆盖
                logging.error("[MLIBER] error: Asset already exist.")
                return
            # 转换缩略图
            self.convert_thumbnail()
            # 创建elements
            if not self.pre_create_elements():
                return
            elements = self.create_elements()
            self.post_create_elements()
            if not elements:
                return
            # 创建asset
            asset = self.create_asset(elements)
            return asset
