# -*- coding: utf-8 -*-
import ix
from mliber_hook.base_hook import BaseHook


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name):
        super(Hook, self).__init__(path, objects, start, end, asset_name)

    def execute(self, *args, **kwargs):
        ix.import_scene(str(self.path))
