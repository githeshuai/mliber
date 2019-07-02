# -*- coding: utf-8 -*-
import os
from mliber_hook.base_hook import BaseHook
from mliber_libs.unreal_libs import asset_export


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name):
        super(Hook, self).__init__(path, objects, start, end, asset_name)

    def execute(self, *args, **kwargs):
        if not self.objects:
            return
        selected_object = self.objects[0]
        selected_object_path = selected_object.get_path_name()
        destination_path = os.path.dirname(self.path)
        asset_export.unreal_export_asset_to_fbx(destination_path, selected_object_path, self.asset_name)
        return self.path
