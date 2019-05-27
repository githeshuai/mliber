# -*- coding: utf-8 -*-
import nuke
from mliber_hook.base_hook import BaseHook
from mliber_libs.nuke_libs import nuke_utils


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name):
        super(Hook, self).__init__(path, objects, start, end, asset_name)

    def execute(self, *args, **kwargs):
        selected_nodes = nuke.selectedNodes()
        if len(selected_nodes) == 1 and selected_nodes[0].Class() == "Read":
            # drop in
            read_node = selected_nodes[0]
            old_read_nodes = nuke.allNodes("Read")
            nuke.tcl("drop", self.directory())
            read_nodes = nuke.allNodes("Read")
            new_read_nodes = list(set(read_nodes) - set(old_read_nodes))
            if len(new_read_nodes) == 1:
                new_read_node = new_read_nodes[0]
                nuke_utils.replace_node(read_node, new_read_node)
                nuke.delete(read_node)
        else:
            nuke.tcl("drop", self.directory())
