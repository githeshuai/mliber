# -*- coding: utf-8 -*-
import os
import re
from Qt.QtGui import QIcon, QPixmap

import mliber_utils
from mliber_conf import mliber_config
from mliber_libs.os_libs.path import Path


def icon_path(path):
    """
    get icon path
    :param path: str
    :return: absolute icon path
    """
    if os.path.isfile(path):
        return path
    icon_dir = mliber_utils.package("mliber_icons")
    return Path(icon_dir).join(path)


def icon(path):
    """
    get icon
    :param path: a icon file path
    :return: QIcon
    """
    path = icon_path(path)
    if Path(path).isfile():
        return QIcon(path)
    return QIcon()


def pixmap(path):
    """
    get pixmap
    :param path: a icon file path
    :return: QPixmap
    """
    path = icon_path(path)
    if Path(path).isfile():
        return QPixmap(path)
    return None


class StyleSheet(object):
    @classmethod
    def from_path(cls, path, **kwargs):
        """
        :type path: str
        :rtype: str
        """
        styleSheet = cls()
        data = styleSheet.read(path)
        data = StyleSheet.format(data, **kwargs)
        styleSheet.set_data(data)
        return styleSheet

    @classmethod
    def from_text(cls, text, options=None):
        """
        :type text: str
        :rtype: str
        """
        styleSheet = cls()
        data = StyleSheet.format(text, options=options)
        styleSheet.set_data(data)
        return styleSheet

    def __init__(self):
        self._data = ''

    def set_data(self, data):
        """
        :type data: str
        """
        self._data = data

    def data(self):
        """
        :rtype: str
        """
        return self._data

    @staticmethod
    def read(path):
        """
        :type path: str
        :rtype: str
        """
        data = ''
        if os.path.isfile(path):
            with open(path, 'r') as f:
                data = f.read()
        return data

    @staticmethod
    def format(data=None, options=None, dpi=1):
        """
        :type data:
        :type options: dict
        :rtype: str
        """
        if options is not None:
            keys = options.keys()
            keys.sort(key=len, reverse=True)
            for key in keys:
                data = data.replace(key, options[key])

        reDpi = re.compile('[0-9]+[*]DPI')
        newData = []
        for line in data.split('\n'):
            dpi_ = reDpi.search(line)
            if dpi_:
                new = dpi_.group().replace('DPI', str(dpi))
                val = int(eval(new))
                line = line.replace(dpi_.group(), str(val))
            newData.append(line)

        data = '\n'.join(newData)
        return data


def style():
    style_dir = mliber_utils.package("mliber_style")
    qss_file = Path(style_dir).join("qss", "style.qss")
    img_dir = Path(style_dir).join("img")
    options = dict(FONT_NAME=mliber_config.FONT_NAME,
                   TITLE_COLOR=mliber_config.TITLE_COLOR,
                   BACKGROUND_COLOR=mliber_config.BACKGROUND_COLOR,
                   ACCENT_COLOR=mliber_config.ACCENT_COLOR,
                   MENU_COLOR=mliber_config.MENU_COLOR,
                   IMG_DIR=img_dir)
    style_sheet = StyleSheet.from_path(qss_file, options=options)
    return style_sheet.data()
