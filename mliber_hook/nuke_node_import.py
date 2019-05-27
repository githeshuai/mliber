# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.nuke_libs.nuke_utils import nuke_import


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name):
        super(Hook, self).__init__(path, objects, start, end, asset_name)

    def execute(self, *args, **kwargs):
        nuke_import(self.path)
        return self.path
