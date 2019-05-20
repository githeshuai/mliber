# -*- coding: utf-8 -*-
"""
parse /mliber_conf/library/{library_type}.yml
"""
import mliber_utils


class Library(object):
    def __init__(self, library_type=""):
        """
        :param library_type: <str>
        """
        self._library_type = library_type
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


if __name__ == "__main__":
    lib = Library("MayaAsset")


