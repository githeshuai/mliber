# -*- coding: utf-8 -*-
"""
parse /mliber_conf/library/{library_type}.yml
"""
import mliber_utils
from mliber_parse.element_type_parser import ElementType


class Library(object):
    def __init__(self, library_type="", engine=""):
        """
        :param library_type: <str>
        :param engine: <str>
        """
        self._library_type = library_type
        self._engine = engine
        self._data = self.parse()

    def library_conf_path(self):
        """
        获取配置文件路径
        :return:
        """
        path = "library/%s.yml" % self._library_type
        return path

    def parse(self):
        """
        get conf data
        :return:
        """

        return mliber_utils.parse(self.library_conf_path())

    def types(self):
        """
        配置的type
        :return:
        """
        return self._data.get("types", [])

    def export_actions(self):
        """
        create actions
        :return: <list>
        """
        types = self.types()
        actions = list()
        for typ in types:
            type_export_actions = ElementType(typ, self._engine).export_actions()
            actions.extend(type_export_actions)
        return actions


if __name__ == "__main__":
    lib = Library("MayaAsset", "maya")
    print len(lib.export_actions())

