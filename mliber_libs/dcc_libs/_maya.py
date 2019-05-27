# -*- coding:utf-8 -*-
from _dcc import Dcc
from mliber_libs.maya_libs import maya_utils


class Maya(Dcc):

    def selected_objects(self):
        return maya_utils.selected_objects()

    def software_info(self):
        return maya_utils.get_maya_version()

    def parent_win(self):
        return maya_utils.get_maya_win()

    def selected_object_names(self):
        return self.selected_objects()
