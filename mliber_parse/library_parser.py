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

    def set_library_type(self, library_type):
        """
        set library
        Returns:
        """
        self._library_type = library_type

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
        data = self.parse()
        if not data:
            print "[LIBER] warning: unknown library type: %s." % self._library_type
            return
        action_list = data.get("create_actions")
        if not action_list:
            print "[LIBER] warning: no create action configured."
            return
        actions = [Action(action_dict) for action_dict in action_list]
        return actions


if __name__ == "__main__":
    lib = Library("MayaAsset")
    for action in lib.actions():
        print action.icon

