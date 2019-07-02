# -*- coding:utf-8 -*-
from _dcc import Dcc
from mliber_libs.unreal_libs import unreal_utils


class Unreal(Dcc):

    def selected_objects(self):
        return unreal_utils.selected_content_objects()

    def software_info(self):
        return unreal_utils.version()

    def parent_win(self):
        return None

    def selected_object_names(self):
        return unreal_utils.selected_content_paths()
