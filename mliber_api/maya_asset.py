# -*- coding:utf-8 -*-
import logging
import pysnooper
from mliber_api.api_utils import find_library, find_category, find_asset, get_thumbnail_type, \
    get_asset_relative_dir, get_thumbnail_pattern, get_texture_dir, get_liber_object_relative_path, add_tag_of_asset
import mliber_global
from mliber_libs.maya_libs.maya_utils import get_maya_version, post_export_textures
from mliber_libs.maya_libs.maya_texture import MayaTexture
from mliber_libs.maya_libs.maya_object_factory import MayaObjectFactory
from mliber_libs.python_libs.sequence_converter import Converter


@pysnooper.snoop()
def create(database_name, library_id, category_id, asset_name, objects, types, start=1, end=1, thumbnail_files=list(),
           tag_names=list(), description="", overwrite=True, export_texture=True,
           recover_texture=True, created_by=None):
    """
    maya资产创建
    :param database_name: custom配置中的database名字
    :param library_id: <int> library id
    :param category_id: <int> category id
    :param asset_name: <str> 资产名字
    :param objects: <list> 需要导出的物体
    :param types: <list> 需要导出哪些类型
    :param thumbnail_files: <list> 缩略图路径，
    :param start: <int> 起始帧
    :param end: <int> 结束帧
    :param tag_names: <list> 标签名字
    :param description: <str> 描述
    :param overwrite: <bool> 如果资产存在,是否覆盖
    :param export_texture: <bool> 是否导出贴图
    :param recover_texture: <bool> 导完贴图之后，当前文件的贴图路径是否需要恢复。
    :param created_by: <int> 创建者ID
    :return:
    """
    software = get_maya_version()
    with mliber_global.db(database_name) as db:
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
        asset = find_asset(db, asset_name, library_id, category_id)
        if asset and not overwrite:  # 如果资产存在，并且不允许覆盖
            logging.error("[MLIBER] error: Asset already exist.")
            return
        # 获取asset相对路径和绝对路径，相对路径存于数据库，绝对路径用来存放导出的东西
        asset_relative_dir = get_asset_relative_dir(category, asset_name)
        asset_abs_dir = asset_relative_dir.format(root=library.root_path())
        # 转换缩略图
        thumbnail_pattern = get_thumbnail_pattern(asset_abs_dir, asset_name)
        thumbnail_type = get_thumbnail_type(thumbnail_files)
        Converter(thumbnail_type).convert(thumbnail_files, thumbnail_pattern)
        print "covert image done."
        logging.info("[MLIBER] info: Convert thumbnail done.")
        # 上传贴图
        if export_texture:
            texture_dir = get_texture_dir(asset_abs_dir)
            texture_info_dict = MayaTexture(objects).export(texture_dir)
            logging.info("[MLIBER] info: Export texture done.")
        # 创建asset和 liber object
        liber_objects = []
        for liber_object_type in types:
            liber_object_relative_path = get_liber_object_relative_path(asset_relative_dir,
                                                                        liber_object_type,
                                                                        asset_name)
            liber_object_abs_path = liber_object_relative_path.format(root=library.root_path())
            maya_object_instance = MayaObjectFactory(liber_object_type).create_instance(liber_object_abs_path)
            try:
                maya_object_instance.export(objects, start=start, end=end)
                plugin = maya_object_instance.plugin_version
                liber_object_name = "{}_{}".format(asset_name, liber_object_type)
                data = {"type": liber_object_type, "software": software, "plugin": plugin,
                        "status": "Active", "path": liber_object_relative_path, "name": liber_object_name}
                if created_by is not None:
                    data.update({"created_by": created_by})
                liber_object = db.create("LiberObject", data)
                liber_objects.append(liber_object)
                logging.info("[MLIBER] info: Export %s done." % liber_object_type)
            except Exception as e:
                logging.error("[MLIBER] error: %s" % str(e))
        if export_texture and recover_texture:
            try:
                post_export_textures(texture_info_dict)
                logging.info("[MLIBER] info: Recover texture settings done.")
            except:
                logging.warning(u"[MLIBER] info: Texture can not be recovered.")
        if not liber_objects:
            return
        # 创建asset
        asset_data = {"name": asset_name, "path": asset_relative_dir, "status": "Active",
                      "library_id": library_id, "category_id": category_id, "description": description,
                      "objects": liber_objects}
        if created_by is not None:
            asset_data.update({"created_by": created_by})
        if not asset:
            asset = db.create("Asset", asset_data)
        else:
            asset = db.update("Asset", asset.id, asset_data)
        logging.info("[MLIBER] info: Create Asset done.")
        # 添加tag
        if tag_names:
            add_tag_of_asset(db, asset, tag_names)
            logging.info("[MLIBER] info: Assign Tag done.")
        return asset
