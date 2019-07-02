# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.unreal_libs import asset_import, unreal_utils


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name):
        super(Hook, self).__init__(path, objects, start, end, asset_name)

    def execute(self, *args, **kwargs):
        destination_path = "/Game/Textures"
        texture_task = asset_import.build_import_task(self.path, destination_path, self.asset_name)
        paths = asset_import.execute_import_tasks([texture_task])
        unreal_utils.select_in_content_browser(paths)
