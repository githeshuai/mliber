# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.maya_libs.maya_objects import MayaFbx
from mliber_libs.maya_libs import maya_utils


class Hook(BaseHook):
    def __init__(self, path, start, end, asset_name=""):
        super(Hook, self).__init__(path, start, end, asset_name)
        self.maya_object = MayaFbx(self.path)
        self.plugin_name = self.maya_object.plugin

    def plugin_version(self):
        return self.maya_object.plugin_version()

    def execute(self, *args, **kwargs):
        objects = maya_utils.selected_objects()
        return self.maya_object.export(objects)
