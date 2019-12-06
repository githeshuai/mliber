#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-12-06 16:04
# Author    : Mr. He
# Version   :
# Usage     : 
# Notes     :

# Import built-in modules
import os
# Import third-party modules

# Import local modules
from mliber_hook.base_hook import BaseHook
from mliber_libs.os_libs.file_opt import copy as cp


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self):
        """
        拷贝到
        :return:
        """
        parent_dir = os.path.dirname(self.path)
        cp(self.source, parent_dir)
        return os.path.dirname(self.path)
