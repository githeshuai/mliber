import logging
import imp
import sys
import os
import mliber_custom
from Qt.QtCore import QSettings
from mliber_libs.os_libs.path import Path
from mliber_libs.python_libs import parser


settings = QSettings("MLIBER", "history")


def root_dir():
    """
    get liber directory
    :return:
    """
    root = Path(__file__).parent()
    root = root.replace("\\", "/")
    return root


def package(package_name):
    """
    get package directory
    :param package_name: str
    :return:
    """
    root = root_dir()
    package_dir = Path(root).join(package_name)
    return package_dir


def parse(conf_file):
    """
    parse
    :param conf_file:
    :return: if conf_file is an exist file, return parse result. else return None
    """
    if not Path(conf_file).isfile():
        conf_dir = package("mliber_conf")
        conf_file = Path(conf_dir).join(conf_file)
    if Path(conf_file).isfile():
        par = parser.Parser(conf_file).parse()
        return par.load()
    return None


def write_history(**kwargs):
    """
    write QSettings
    Args:
        **kwargs:
    Returns:
    """
    for key, value in kwargs.iteritems():
        settings.setValue(key, value)


def read_history(key):
    """
    read QSettings value
    Args:
        key:
    Returns:
    """
    return settings.value(key)


def load_module(name, paths):
    """
    :param name: module name
    :param paths:directory <str> or <list>
    :return:
    """
    if isinstance(paths, basestring):
        paths = [paths]
    try:
        fn_, path, desc = imp.find_module(name, paths)
        mod = imp.load_module(name, fn_, path, desc)
        return mod
    except ImportError as e:
        logging.error(str(e))


def load_hook(name):
    """
    :param name: module name<str>
    :return:
    """
    hook_dir = mliber_custom.HOOK_DIR
    liber_hook_dir = package("mliber_hook")
    hook_dir.append(liber_hook_dir)
    mod = load_module(name, hook_dir)
    return mod


if __name__ == "__main__":
    print load_hook("maya_ma_export")
