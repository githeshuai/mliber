# -*- coding:utf-8 -*-
from mliber_api.mliber.api_utils import find_library, find_category, find_asset
import mliber_resource
import mliber_global
from mliber_libs.maya_libs.maya_object_factory import MayaObjectFactory


def create(database_name, library_id, category_id, asset_name, types, start=1, end=1, thumbnail_files=list(),
           tag_names=list(), description="", overwrite=True, export_texture=True,
           recover_texture=True):
    """
    maya资产创建
    :param database_name: custom配置中的database名字
    :param library_id: <int> library id
    :param category_id: <int> category id
    :param asset_name: <str> 资产名字
    :param types: <list> 需要导出哪些类型
    :param thumbnail_files: <缩略图路径>
    :param start: <int> 起始帧
    :param end: <int> 结束帧
    :param tag_names: <list> 标签名字
    :param description: <str> 描述
    :param overwrite: <bool> 如果资产存在,是否覆盖
    :param export_texture: <bool> 是否导出贴图
    :param recover_texture: <bool> 导完贴图之后，当前文件的贴图路径是否需要恢复。
    :return:
    """
    with mliber_global.db(database_name) as db:
        # 确保library存在
        library = find_library(db, library_id)
        if not library:
            print "[MLIBER] error: library not exist."
            return
        # 确保category存在
        category = find_category(db, category_id)
        if not category:
            print "[MLIBER] error: category not exist."
            return
        # 判断资产是否存在
        asset = find_asset(db, asset_name, library_id, category_id)
        if asset and not overwrite:  # 如果资产存在，并且不允许覆盖
            print "资产已存在"
            return
        # 转换缩略图

        # 上传贴图

        # 创建asset和 liber object