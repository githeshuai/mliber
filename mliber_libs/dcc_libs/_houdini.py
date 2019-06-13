# -*- coding:utf-8 -*-
from _dcc import Dcc
from mliber_libs.houdini_libs import houdini_utils


class Houdini(Dcc):

    def selected_objects(self):
        return houdini_utils.selected()

    def software_info(self):
        return houdini_utils.version()

    def parent_win(self):
        return houdini_utils.parent_win()

    def selected_object_names(self):
        node_names = list()
        selected_nodes = self.selected_objects()
        if selected_nodes:
            for node in selected_nodes:
                node_names.append(node.path())
        return node_names

