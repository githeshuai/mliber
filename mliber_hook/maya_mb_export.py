# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.maya_libs.maya_objects import MayaFile


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name=""):
        super(Hook, self).__init__(path, objects, start, end, asset_name)

    def execute(self, *args, **kwargs):
        return MayaFile(self.path).export(self.objects)
