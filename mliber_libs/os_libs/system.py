# -*- coding: utf-8 -*-
import os
import subprocess
import platform
from datetime import datetime


def system():
    """
    :rtype: str
    """
    return platform.system().lower()


def is_mac():
    """
    :rtype: bool
    """
    return system().startswith('mac') or system().startswith('os') or system().startswith('darwin')


def is_windows():
    """
    :rtype: bool
    """
    return system().startswith('win')


def is_linux():
    """
    :rtype: bool
    """
    return system().startswith('lin')


def operation_system():
    """
    get operation system windows or linux or mac
    :return:
    """
    if is_windows():
        return "windows"
    elif is_linux():
        return "linux"
    else:
        return "mac"


def open_location(path):
    """
    :type path: str
    :rtype: None
    """
    if is_linux():
        os.system('xdg-open %s' % path)
    elif is_windows():
        try:
            os.startfile('%s' % path)
        except:
            os.startfile(os.path.dirname(path))
    elif is_mac():
        subprocess.call(['open', '-R', path])


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    print now()

