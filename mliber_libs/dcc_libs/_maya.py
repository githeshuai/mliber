# -*- coding:utf-8 -*-
import maya.cmds as mc
from _dcc import Dcc
from mliber_libs.maya_libs import maya_utils


class Maya(Dcc):

    def selected_objects(self):
        return mc.ls(sl=1)

    def software_info(self):
        return maya_utils.get_maya_version()

    def parent_win(self):
        return maya_utils.get_maya_win()
