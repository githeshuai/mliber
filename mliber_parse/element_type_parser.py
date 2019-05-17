# -*- coding: utf-8 -*-
"""
parse /mliber_conf/element_type/{element_type}.yml
"""
import mliber_utils
from mliber_libs.os_libs.path import Path


class ElementType(object):
    def __init__(self, element_type=""):
        """
        init
        :param element_type:
        """
        self._type = element_type
        self._data = self.parse()

    def element_type_conf_path(self):
        """
        获取配置文件路径
        :return:
        """
        path = "element_type/%s.yml" % self._type
        return path

    def parse(self):
        """
        get conf data
        :return:
        """

        return mliber_utils.parse(self.element_type_conf_path())

    def actions(self):
        """
        apply actions
        :return:
        """
        return

    def __getattr__(self, item):
        """

        :param item:
        :return:
        """
        if not self._data:
            print "[MLIBER] warning: unknown element type: %s." % self._type
            return
        if item == "icon":
            icon = self._data.get("icon")
            icon_dir = mliber_utils.package("mliber_icons")
            if not icon:
                return Path(icon_dir).join("action_icons/default.png")
            if Path(icon).isfile():
                return icon
            if icon == "default":
                icon = Path(icon_dir).join("action_icons/default.png")
            else:
                icon = Path(icon_dir).join(icon)
            if not Path(icon).isfile():
                icon = Path(icon_dir).join("action_icons/default.png")
            return icon
        return self._data.get(item, None)


if __name__ == "__main__":
    p = ElementType("ma")
    print p.parse()
