# -*- coding: utf-8 -*-


class Action(object):
    def __init__(self, action_dict):
        """
        __init__ builtin
        create or apply actions
        :param action_dict: {"name": "maya abc export", "hook": "maya_abc_export", "checked": False, "icon": "default"}
        """
        self.action_dict = action_dict

    def __getattr__(self, item):
        return self.action_dict.get(item)
