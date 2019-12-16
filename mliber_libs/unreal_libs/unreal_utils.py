# -*- coding:utf-8 -*-
import unreal


def selected_content_objects():
    """
    获取content browser中选中的物体对象
    :return:
    """
    utility_base = unreal.GlobalEditorUtilityBase.get_default_object()
    selected_assets = utility_base.get_selected_assets()
    assets = list(selected_assets)
    return assets


def selected_content_paths():
    """
    获取Content Browser中选中物体的path
    :return:
    """
    assets = selected_content_objects()
    paths = [asset.get_path_name() for asset in assets]
    return paths


def version():
    """
    获取当前unreal版本
    :return:
    """
    version_str = unreal.SystemLibrary.get_engine_version()
    version_name = version_str.split("-")[0]
    return "unreal_%s" % version_name


def select_in_content_browser(paths):
    """
    在Content Browser中选择物体
    :param paths: <list> Content Browser paths
    :return:
    """
    if not paths:
        return
    if isinstance(paths, basestring):
        paths = [paths]
    unreal.EditorAssetLibrary.sync_browser_to_objects(paths)
