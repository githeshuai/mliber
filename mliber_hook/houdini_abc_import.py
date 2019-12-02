# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.houdini_libs import houdini_utils


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self, *args, **kwargs):
        houdini_utils.import_abc(self.path, node_name=self.asset_name)
