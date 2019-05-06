# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import datetime
import system
import file_opt
from mliber_custom.path_opt import PathOperator


class Path(object):
    def __init__(self, path=None):
        self.path = path.replace("\\", "/")

    def absolute(self):
        """
        get abs path
        :return:
        """
        return os.path.abspath(self.path)

    def exists(self):
        """
        :return: bool
        """
        return os.path.exists(self.path)

    def isdir(self):
        """
        :return: bool
        """
        return os.path.isdir(self.path)

    def isfile(self):
        """
        :return: bool
        """
        return os.path.isfile(self.path)

    def makedirs(self):
        """
        :return: None
        """
        if os.path.isdir(self.path):
            return
        PathOperator(self.path).pre_create()
        os.makedirs(self.path)
        PathOperator(self.path).post_create()

    def make_parent_dir(self):
        """
        创建父级目录
        :return:
        """
        parent_dir = self.parent()
        if not os.path.isdir(parent_dir):
            PathOperator(parent_dir).pre_create()
            os.makedirs(parent_dir)
            PathOperator(parent_dir).post_create()

    def remove(self):
        """
        :return: None
        """
        PathOperator(self.path).pre_delete()
        if self.isdir():
            shutil.rmtree(self.path)
        elif self.isfile():
            os.remove(self.path)
        PathOperator(self.path).post_delete()

    def dirname(self):
        """
        :return: str
        """
        return os.path.dirname(self.path)

    def children(self):
        """
        :return: list
        """
        from mliber_conf import mliber_config
        paths = list()
        if self.isdir():
            all_children = os.listdir(self.path)
            for i in mliber_config.IGNORE_LIST:
                try:
                    all_children.remove(i)
                except:pass
            for each in all_children:
                paths.append("{0}/{1}".format(self.path, each).replace("\\", "/"))
        return paths

    def listdir(self):
        """
        list dir
        :return:
        """
        if self.isdir():
            return os.listdir(self.path)
        return []

    def has_children(self):
        """
        :return:bool
        """
        if self.isdir():
            return True if os.listdir(self.path) else False
        return False

    def rename(self, name):
        """
        :param name: str
        :return: bool
        """
        if self.exists():
            os.rename(self.path, name)
            return True
        return False

    def basename(self):
        """
        base name
        :return:
        """
        return os.path.basename(self.path)

    def filename(self):
        """
        file name
        :return:
        """
        return os.path.splitext(self.basename())[0]

    def join(self, *args):
        """
        join
        :param args:
        :return:
        """
        path = os.path.abspath(os.path.join(self.path, *args))
        path = path.replace("\\", "/")
        return path

    def ext(self):
        """
        ext
        :return:
        """
        return os.path.splitext(self.path)[-1]

    def stem(self):
        """
        file name without ext.
        :return:
        """
        return os.path.splitext(self.path)[0]

    def splitdrive(self):
        """
        :return:
        """
        return os.path.splitdrive(self.path)

    def parent(self):
        """
        parent
        :return:
        """
        return os.path.dirname(self.path)

    def ancestor(self, num):
        """
        ancestor
        :param num:
        :return:
        """
        an = os.path.abspath(os.path.join(self.path, "../" * num))
        an = an.replace("\\", "/")
        return an

    def open(self):
        """
        open location
        :return:
        """
        system.open_location(self.path)

    def copy_to(self, target):
        """
        copy path or file to target directory
        :param target: str <an exist file or directory>
        :return:
        """
        file_opt.copy(self.path, target)

    def getctime(self):
        """
        get create time
        :return:
        """
        create_time = os.path.getctime(self.path)
        date = datetime.datetime.fromtimestamp(create_time)
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def getmtime(self):
        """
        get latest modify time
        :return:
        """
        modify_time = os.path.getmtime(self.path)
        date = datetime.datetime.fromtimestamp(modify_time)
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def size(self):
        """
        获取文件大小
        :return:
        """
        return os.path.getsize(self.path)

    def __call__(self):
        return self.path


if __name__ == "__main__":
    print Path(__file__).parent()
