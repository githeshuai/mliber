#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-12-16 14:57
# Author    : Mr.He
# Usage     : 
# Version   :
# Comment   :


# Import built-in modules

# Import third-party modules

# Import local modules
import mliber_custom
from mliber_libs.os_libs.path import Path
from mliber_libs.python_libs.parser import Parser
from mliber_libs.os_libs.system import operation_system


class Settings(object):
    def __init__(self, user_name):
        """
        built in
        :param user_name:
        """
        self._user_name = user_name
        self._public_dir = mliber_custom.PUBLIC_PATH.get(operation_system())
        self._data = self.settings_data()

    def settings_dir(self):
        """
        存放用户数据的目录
        :return:
        """
        return Path(self._public_dir).join("settings/%s" % self._user_name)

    def settings_file(self):
        """
        存放用户数据的json文件
        :return:
        """
        file_name = "settings.json"
        setting_dir = self.settings_dir()
        return Path(setting_dir).join(file_name)

    def settings_file_exist(self):
        """
        判断settings.json文件是否存在
        :return:
        """
        return Path(self.settings_file()).isfile()

    def settings_data(self):
        """
        json settings data
        :return: <dict>
        """
        if self.settings_file_exist():
            return Parser(self.settings_file()).parse().load()
        return {}

    def set(self, key, value):
        """
        set settings data
        :param key: <str>
        :param value: <str>
        :return:
        """
        self._data[key] = value

    def update(self, data):
        """
        update
        :param data: <dict>
        :return:
        """
        for key, value in data.iteritems():
            self.set(key, value)

    def get(self, key):
        """
        get settings data
        :param key: <str>
        :return:
        """
        settings_data = self._data
        return settings_data.get(key, None)

    def write_out(self):
        """
        write out the settings
        :return:
        """
        Parser(self.settings_file()).parse().dump(self._data)

    def max_icon_size(self):
        """
        get max icon size
        :return: <int>
        """
        return self.get("max_icon_size") or mliber_custom.THUMBNAIL_SIZE

    def paint_description(self):
        """
        get whether paint description on asset icon
        :return: <bool>
        """
        whether_paint_description = self.get("paint_description")
        return mliber_custom.PAINT_DESCRIPTION if whether_paint_description is None else whether_paint_description

    def paint_color(self):
        """
        get paint description color
        :return:
        """
        return self.get("paint_color") or mliber_custom.DESCRIPTION_COLOR

    def paint_size(self):
        """
        get paint description size
        :return:
        """
        return self.get("paint_size") or mliber_custom.DESCRIPTION_FONT_SIZE

    def show_asset_flag(self):
        """
        get whether show flags on asset icon
        :return:
        """
        whether_show_asset_flag = self.get("show_asset_flag")
        return mliber_custom.SHOW_ASSET_FLAG if whether_show_asset_flag is None else whether_show_asset_flag

    def show_asset_name(self):
        """
        whether show asset name on asset icon
        :return:
        """
        whether_show_asset_name = self.get("show_asset_name")
        return mliber_custom.SHOW_ASSET_NAME if whether_show_asset_name is None else whether_show_asset_name
