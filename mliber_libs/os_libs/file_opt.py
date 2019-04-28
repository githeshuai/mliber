# -*- coding: utf-8 -*-
import os
import shutil
import filecmp
from distutils.dir_util import copy_tree


def copy(src, dst):
    """
    copy file or directory
    :param src: str <source file or directory>
    :param dst: dst <target file or directory>
    :return:
    """
    if os.path.isfile(src):
        copy_file(src, dst)
    elif os.path.isdir(src):
        copy_tree(src, dst)


def copy_file(src, dst):
    """
    :param src: source file
    :param dst: destination file
    :return:
    """
    dst_dir = os.path.dirname(dst)
    if (not src) or (not os.path.isfile(src)):
        print "%s is not an exist file" % src
        return False
    if os.path.isfile(dst):
        if filecmp.cmp(src, dst):
            print "%s and %s is the same." % (src, dst)
            return True
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    shutil.copyfile(src, dst)
    return True

