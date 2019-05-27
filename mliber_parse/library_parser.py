# -*- coding: utf-8 -*-
"""
parse /mliber_conf/library/{library_type}.yml
"""
import mliber_utils


class Library(object):
    pool = dict()
    __init = False

    def __new__(cls, library_type=""):
        obj = cls.pool.get(library_type, None)
        if not obj:
            obj = object.__new__(cls)
            cls.pool[library_type] = obj
        return obj

    def __init__(self, library_type=""):
        """
        :param library_type: <str>
        """
        if not self.__init:
            self._library_type = library_type
            self._data = self.parse()
            self.__init = True

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

    def double_clicked_type(self):
        """
        双击运行的type
        :return:
        """
        return self._data.get("double_clicked", {}).get("type")

    def double_clicked_hook(self):
        """
        双击运行的hook
        :return:
        """
        return self._data.get("double_clicked", {}).get("hook")

    def need_check_selected(self):
        """
        是否需要检查选择节点
        :return:
        """
        return self._data.get("check_selected")

    def show_frame_range(self):
        """
        是否需要显示frame range
        :return:
        """
        return self._data.get("show_frame_range")


if __name__ == "__main__":
    print Library("MayaAsset").double_clicked_hook()


