# -*- coding: utf-8 -*-
import mliber_utils
from mliber_libs.os_libs.path import Path


class Action(object):
    def __init__(self, action_dict):
        """
        __init__ builtin
        create or apply actions
        :param action_dict: {"name": "maya abc export", "hook": "maya_abc_export", "checked": False, "icon": "default"}
        """
        self.action_dict = action_dict

    def __getattr__(self, item):
        if item == "icon":
            icon = self.action_dict.get("icon")
            if Path(icon).isfile():
                return icon
            icon_dir = mliber_utils.package("mliber_icons")
            if icon == "default":
                icon = Path(icon_dir).join("action_icons/default.png")
            else:
                icon = Path(icon_dir).join(icon)
            if not Path(icon).isfile():
                icon = Path(icon_dir).join("action_icons/default.png")
            return icon
        return self.action_dict.get(item)
