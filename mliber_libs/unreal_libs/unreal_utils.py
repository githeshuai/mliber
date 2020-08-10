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


def save_asset(path, force_save=True):
    """
    保存资产
    :param path: asset path
    :param force_save: True if the operation succeeds
    :return:
    """
    return unreal.EditorAssetLibrary.save_asset(asset_to_save=path, only_if_is_dirty=not force_save)


def save_directory(path, force_save=True, recursive=True):
    """
    保存目录
    :param path: <str> directory path
    :param force_save:
    :param recursive:
    :return:
    """
    return unreal.EditorAssetLibrary.save_directory(directory_path=path,
                                                    only_if_is_dirty=not force_save,
                                                    recursive=recursive)


def get_package_from_path(path):
    return unreal.load_package(path)


def get_all_dirty_packages():
    """
    获取没有保存的
    :return:
    """
    packages = []
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
        packages.append(x)
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages():
        packages.append(x)
    return packages


def save_all_dirty_packages(show_dialog=False):
    """
    保存所有脏的包
    :param show_dialog:
    :return:
    """
    if show_dialog:
        return unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(True, True)
    return unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)


def save_packages(packages, show_dialog=False):
    """
    保存指定的包
    :param packages:
    :param show_dialog:
    :return:
    """
    if show_dialog:
        return unreal.EditorLoadingAndSavingUtils.save_packages_with_dialog(packages, only_dirty=True)
    return unreal.EditorLoadingAndSavingUtils.save_packages(packages, only_dirty=True)


def directory_exists(directory):
    """
    判断目录是否存在
    :param directory:
    :return:
    """
    return unreal.EditorAssetLibrary.does_directory_exist(directory)


def create_directory(directory):
    """
    创建目录
    :param directory:
    :return:
    """
    return unreal.EditorAssetLibrary.make_directory(directory)


def duplicate_directory(directory, dst_directory):
    """
    复制目录
    :param directory:
    :param dst_directory:
    :return:
    """
    return unreal.EditorAssetLibrary.duplicate_directory(directory, dst_directory)


def delete_directory(directory):
    """
    删除目录
    :param directory:
    :return:
    """
    return unreal.EditorAssetLibrary.delete_directory(directory)


def rename_directory(directory, new_directory):
    """
    重命名目录
    :param directory:
    :param new_directory:
    :return:
    """
    return unreal.EditorAssetLibrary.rename_directory(directory, new_directory)


def asset_exist(asset_path):
    return unreal.EditorAssetLibrary.does_asset_exist(asset_path)


def duplicate_asset(asset, new_path):
    return unreal.EditorAssetLibrary.duplicate_asset(asset, new_path)


def delete_asset(asset):
    return unreal.EditorAssetLibrary.delete_asset(asset)


def duplicate_asset_with_dialog(origin_asset, new_package_path, new_asset_name, show_dialog=True):

    if show_dialog:
        return unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset_with_dialog(asset_name=new_asset_name,
                                                                                      packages_path=new_package_path,
                                                                                      origin_object=unreal.load_asset(origin_asset))
    else:
        unreal.duplicate_asset.get_asset_tools().duplicate_asset(asset_name=new_asset_name,
                                                                 packages_path=new_package_path,
                                                                 origin_object=unreal.load_asset(origin_asset))


def rename_asset(asset, new_asset):
    unreal.EditorAssetLibrary.rename_asset(asset, new_asset)


