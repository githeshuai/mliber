# -*- coding:utf-8 -*-
from mliber_libs.maya_libs import maya_utils


class MayaObject(object):
    def __init__(self, path):
        self.path = path

    def export(self, *args, **kwargs):
        """
        导出
        :param args:
        :param kwargs:
        :return:
        """
        return self.path

    def import_in(self, *args, **kwargs):
        """
        导入
        :param args:
        :param kwargs:
        :return:
        """
        return

    @property
    def plugin_version(self):
        if hasattr(self, "plugin"):
            return maya_utils.get_plugin_version(self.plugin)
