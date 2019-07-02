# -*- coding:utf-8 -*-
import os
import unreal


def unreal_export_asset_to_fbx(destination_path, asset_path, asset_name):
    """
    Export an asset to FBX from Unreal

    :param destination_path: The path where the exported FBX will be placed
    :param asset_path: The Unreal asset to export to FBX
    :param asset_name: The asset name to use for the FBX filename
    """
    # Get an export task
    task = generate_fbx_export_task(destination_path, asset_path, asset_name)
    if not task:
        return False, None

    # Do the FBX export
    result = unreal.Exporter.run_asset_export_task(task)

    if not result:
        unreal.log_error("Failed to export {}".format(task.filename))
        for error_msg in task.errors:
            unreal.log_error("{}".format(error_msg))

        return result, None

    return result, task.filename


def generate_fbx_export_task(destination_path, asset_path, asset_name):
    """
    Create and configure an Unreal AssetExportTask

    :param destination_path: The path where the exported FBX will be placed
    :param asset_path: The Unreal asset to export to FBX
    :param asset_name: The FBX filename to export to
    :return the configured AssetExportTask
    """
    loaded_asset = unreal.EditorAssetLibrary.load_asset(asset_path)

    if not loaded_asset:
        unreal.log_error(
            "Failed to create FBX export task for {}: Could not load asset {}".format(asset_name, asset_path))
        return None

    filename = os.path.join(destination_path, asset_name + ".fbx")

    # Setup AssetExportTask for non-interactive mode
    task = unreal.AssetExportTask()
    task.object = loaded_asset  # the asset to export
    task.filename = filename  # the filename to export as
    task.automated = True  # don't display the export options dialog
    task.replace_identical = True  # always overwrite the output

    # Setup export options for the export task
    task.options = unreal.FbxExportOption()
    # These are the default options for the FBX export
    # task.options.fbx_export_compatibility = fbx_2013
    # task.options.ascii = False
    # task.options.force_front_x_axis = False
    # task.options.vertex_color = True
    # task.options.level_of_detail = True
    # task.options.collision = True
    # task.options.welded_vertices = True
    # task.options.map_skeletal_motion_to_root = False

    return task
