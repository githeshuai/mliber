# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
import hou


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self, *args, **kwargs):
        selected_nodes = hou.selectedNodes()
        if not selected_nodes:
            self.append_error("No houdini node selected.")
            return
        node = selected_nodes[0]
        gen = node.parm('env_map')
        if gen is None:
            gen = node.parm('ar_light_color_texture')
        if gen is None:
            gen = node.parm('A_FILENAME')
        gen.set(self.path)
