# -*- coding:utf-8 -*-
from _dcc import Dcc
from mliber_libs.nuke_libs import nuke_utils


class Nuke(Dcc):

    def selected_objects(self):
        return nuke_utils.selected_nodes()

    def software_info(self):
        return nuke_utils.version()

    def parent_win(self):
        return nuke_utils.parent_window()

    def selected_object_names(self):
        node_names = list()
        selected_nodes = self.selected_objects()
        if selected_nodes:
            for node in selected_nodes:
                node_names.append(node.name())
        return node_names
