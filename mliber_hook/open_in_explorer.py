# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.os_libs.path import Path


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self, *args, **kwargs):
        parent_dir = Path(self.path).parent()
        Path(parent_dir).open()
