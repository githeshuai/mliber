# -*- coding: utf-8 -*-
import ix
from mliber_hook.base_hook import BaseHook
from mliber_libs.clarisse_libs import clarisse_utils


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name):
        super(Hook, self).__init__(path, objects, start, end, asset_name)

    def execute(self, *args, **kwargs):
        selected = ix.selection
        if selected and selected.get_count() == 1:
            if selected[0].get_class().get_name() == "TextureMapFile":
                selected[0].attrs.filename = str(self.path)
                return
        clarisse_utils.create_ibl(str(self.path))
