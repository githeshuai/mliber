# -*- coding: utf-8 -*-
import logging


class BaseHook(object):
    logger = logging.getLogger("Hook")

    def __init__(self, typ, asset_name, path, start, end):
        """
        :param typ: <str> Element type
        :param asset_name: <str>
        :param path: <str> 需要导出或者导入的文件路径
        :param start: <int> 起始帧
        :param end: <int> 结束帧
        """
        self.type = typ
        self.asset_name = asset_name
        self.path = path
        self.start = start
        self.end = end
        self._error_list = []

    @property
    def error_str(self):
        """
        error string
        :return:
        """
        return "\n".join(self._error_list)

    def execute(self, *args, **kwargs):
        """
        what need to do
        :return:
        """
        pass

    def main(self, *args, **kwargs):
        """
        main function
        :return:
        """
        try:
            path = self.execute(*args, **kwargs)
            return path
        except RuntimeError as e:
            self._error_list.append(str(e))
        if self.error_str:
            self.logger.error(self.error_str)
