# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.maya_libs.maya_objects import MayaAbc


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)
        self.maya_object = MayaAbc(self.path)

    def execute(self, *args, **kwargs):
        return self.maya_object.import_in()
