#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-12-17 15:05
# Author    : Mr.He
# Usage     : 
# Version   :
# Comment   :


# Import built-in modules
import subprocess
# Import third-party modules

# Import local modules
from mliber_hook.base_hook import BaseHook


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self, *args, **kwargs):
        cmd = "rez env %s %s -- maya %s" % (self.software(), self.plugin(), self.path)
        subprocess.Popen(cmd, shell=True)
