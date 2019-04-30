# -*- coding:utf-8 -*-
import sys
from Qt.QtWidgets import QApplication


class Global(object):
    __has_inited = False

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self):
        if not self.__has_inited:
            self.__dict = dict()
            self.__has_inited = True

    def set_value(self, **kwargs):
        """
        :return:
        """
        for key, value in kwargs.iteritems():
            self.__dict[key] = value

    def value(self, key):
        """
        get global value
        :param key:
        :return:
        """
        return self.__dict.get(key)


def get_app_global():
    """
    获取全局变量
    :return:
    """
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.globals = Global()
    return app.globals


if __name__ == "__main__":
    app_global = get_app_global()
    app_global.set_value(a=1, b=2)
    print app_global.value("a")
    print app_global.value("b")
