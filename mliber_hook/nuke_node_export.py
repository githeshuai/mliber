# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.nuke_libs.nuke_utils import export_selected


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name):
        super(Hook, self).__init__(path, objects, start, end, asset_name)

    def execute(self, *args, **kwargs):
        export_selected(self.path)
        return self.path
