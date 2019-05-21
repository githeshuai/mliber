# -*- coding: utf-8 -*-
import logging


class BaseHook(object):
    logger = logging.getLogger("Hook")

    def __init__(self, path, start, end, asset_name=""):
        """
        :param path: <str> 需要导出或者导入的文件路径
        :param start: <int> 起始帧
        :param end: <int> 结束帧
        :param asset_name: <str> 资产名字
        """
        self.asset_name = asset_name
        self.path = path
        self.start = start
        self.end = end
        # custom
        self.plugin_name = ""
        self._error_list = []

    def plugin_version(self):
        """
        获取插件方法, 默认返回插件名字，子类可重写
        :return:
        """
        return self.plugin_name

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
            result = self.execute(*args, **kwargs)
        except RuntimeError as e:
            self._error_list.append(str(e))
            result = None
        if self.error_str:
            self.logger.error(self.error_str)
        return result