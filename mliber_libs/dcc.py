# -*- coding:utf-8 -*-
import os
import sys


class Dcc(object):
    def __init__(self):
        """
        built in
        """
        self._engine = self.engine()

    @staticmethod
    def engine():
        """
        :return: <str>
        """
        app = sys.executable
        app_basename = os.path.basename(app)
        app_name = os.path.splitext(app_basename)[0]
        if "Nuke" in app_name:
            app_name = "nuke"
        elif "houdini" in app_name:
            app_name = "houdini"
        elif "maya" in app_name:
            app_name = "maya"
        elif "clarisse" in app_name:
            app_name = "clarisse"
        else:
            app_name = "standalone"
        return app_name

    @classmethod
    def software(cls):
        """
        获取软件名字及版本
        :return:
        """
        if cls.engine() == "maya":
            from mliber_libs.maya_libs import maya_utils
            return maya_utils.get_maya_version()
        return ""


if __name__ == "__main__":
    print Dcc.software()
