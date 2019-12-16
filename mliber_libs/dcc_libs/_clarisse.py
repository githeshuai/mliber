# -*- coding:utf-8 -*-
import ix
from _dcc import Dcc


class Clarisse(Dcc):

    def selected_objects(self):
        return ix.selection

    def selected_object_names(self):
        node_names = list()
        for node in self.selected_objects():
            name = node.get_full_name()
            node_names.append(name)
        return node_names

    def software_info(self):
        return "clarisse"

    def parent_win(self):
        return

