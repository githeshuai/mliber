# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.unreal_libs import asset_import, unreal_utils
from mliber_qt_components.unreal_import_options_widget import UnrealImportOptionsWidget


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self, *args, **kwargs):
        widget = UnrealImportOptionsWidget()
        widget.exec_()
        as_skeletal, materials, textures = widget.as_skeletal, widget.materials, widget.textures
        if as_skeletal is None and materials is None and textures is None:
            return
        destination_path = "/Game/SkeletonMeshes" if as_skeletal else "/Game/StaticMeshes"
        options = asset_import.build_fbx_import_options(as_skeletal, materials, textures)
        skeleton_task = asset_import.build_import_task(self.path, destination_path, self.asset_name, options)
        paths = asset_import.execute_import_tasks([skeleton_task])
        unreal_utils.select_in_content_browser(paths)
