# -*- coding:utf-8 -*-


class PathOperator(object):
    def __init__(self, path):
        """
        built in
        :param path: <str> full path
        """
        self.path = path

    def pre_create(self):
        """
        在创建文件夹前执行的操作，比如会用xmlrpc解开父级权限
        :return:
        """
        return

    def post_create(self):
        """
        在创建文件夹之后执行的操作，比如xmlrpc锁定文件夹权限
        :return:
        """
        return

    def pre_delete(self):
        """
        删除文件或者文件夹之前执行的操作
        :return:
        """
        return

    def post_delete(self):
        """
        删除文件夹之后执行的操作
        :return:
        """
        return

    def rename(self, new_name):
        """
        重命名
        :param new_name: only new basename
        :return:
        """
        return
