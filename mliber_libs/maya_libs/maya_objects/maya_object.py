# -*- coding:utf-8 -*-
from mliber_libs.maya_libs import maya_utils


class MayaObject(object):
    def __init__(self, path):
        self.path = path
        self.plugin = None

    def load_plugin(self):
        """
        加载插件
        :return:
        """
        return maya_utils.load_plugin(self.plugin)

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

    def plugin_version(self):
        if self.plugin:
            return maya_utils.get_plugin_version(self.plugin)
