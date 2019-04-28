# -*- coding:utf-8 -*-
import sys
from Qt.QtWidgets import QApplication


class Global(object):
    def __init__(self):
        self.__dict = dict()

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
