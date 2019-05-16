# -*- coding: utf-8 -*-
"""
parse /mliber_conf/library/{library_type}.yml
"""
from action import Action
import mliber_utils


class Library(object):
    def __init__(self, library_type=""):
        """
        initialize
        Args:
            library_type: <str> library type
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

    def actions(self):
        """
        create actions
        :return:
        """
        action_list = self.create_actions
        if not action_list:
            print "[MLIBER] warning: no create action configured."
            return
        actions = [Action(action_dict) for action_dict in action_list]
        return actions

    def __getattr__(self, item):
        """

        :param item:
        :return:
        """
        if not self._data:
            print "[MLIBER] warning: unknown library type: %s." % self._library_type
            return
        return self._data.get(item, None)


if __name__ == "__main__":
    lib = Library("MayaAsset")
    for action in lib.actions():
        print action.icon

