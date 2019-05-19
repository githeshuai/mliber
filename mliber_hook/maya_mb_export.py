# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.maya_libs.maya_objects import MayaFile
from mliber_libs.maya_libs import maya_utils


class Hook(BaseHook):
    def __init__(self, path, start, end, asset_name=""):
        super(Hook, self).__init__(path, start, end, asset_name)

    def execute(self, *args, **kwargs):
        objects = maya_utils.selected_objects()
        return MayaFile(self.path).export(objects)
