# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.maya_libs.maya_objects import MayaXgenProxy


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)
        self.maya_object = MayaXgenProxy(self.path)

    def execute(self, *args, **kwargs):
        self.maya_object.import_in()
