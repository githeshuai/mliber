# -*- coding:utf-8 -*-
from dcc_factory import DccFactory
from mliber_utils import get_engine


class Dcc(object):
    def __init__(self, engine=None):
        """
        built in
        :param engine: <str> 软件名字
        """
        self._engine = engine or get_engine()
        self._dcc = DccFactory(self._engine).create()

    @classmethod
    def engine(cls):
        return cls()._engine

    def software(self):
        """
        获取软件名字及版本
        :return:
        """
        return self._dcc.software_info()

    def selected_objects(self):
        """
        获取选择的物体
        :return:
        """
        return self._dcc.selected_objects()

    def parent_win(self):
        """
        获取父窗口
        :return:
        """
        return self._dcc.parent_win()


if __name__ == "__main__":
    print Dcc.engine()
