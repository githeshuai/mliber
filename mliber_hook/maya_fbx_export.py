# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.maya_libs.maya_objects import MayaFbx
from mliber_libs.maya_libs import maya_utils


class Hook(BaseHook):
    def __init__(self, typ, asset_name, path, start, end):
        super(Hook, self).__init__(typ, asset_name, path, start, end)

    def execute(self, *args, **kwargs):
        objects = maya_utils.selected_objects()
        MayaFbx(self.path).export(objects)
