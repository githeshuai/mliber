# -*- coding: utf-8 -*-
"""
parse /mliber_conf/liber_object_type/{liber_object_type}.yml
"""
import mliber_utils


class ElementType(object):
    def __init__(self, liber_object_type=""):
        """
        init
        :param liber_object_type:
        """
        self._type = liber_object_type
        self._data = self.parse()

    def liber_object_type_conf_path(self):
        """
        获取配置文件路径
        :return:
        """
        path = "liber_object_type/%s.yml" % self._type
        return path

    def parse(self):
        """
        get conf data
        :return:
        """

        return mliber_utils.parse(self.liber_object_type_conf_path())

    def apply_actions(self):
        """
        apply actions
        :return:
        """

    def __getattr__(self, item):
        """

        :param item:
        :return:
        """
        if not self._data:
            print "[MLIBER] warning: unknown liber object type: %s." % self._type
            return
        return self._data.get(item, None)


if __name__ == "__main__":
    p = ElementType("ma")
    print p.parse()
