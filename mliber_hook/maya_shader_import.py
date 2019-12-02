# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from mliber_hook.base_hook import BaseHook
from mliber_libs.maya_libs import maya_utils


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self, *args, **kwargs):
        path = self.path
        if not os.path.isfile(path):
            self.append_error("%s is not an exist file." % path)
            return
        sels = maya_utils.selected_objects()
        if not sels:
            self.append_error("Nothing selected")
            return
        old_sg_nodes = mc.ls(type="shadingEngine")
        maya_utils.maya_import(self.path)
        new_sg_nodes = mc.ls(type="shadingEngine")
        sg_node = list(set(new_sg_nodes) - set(old_sg_nodes))
        if not sg_node:
            self.append_error("No shadingEngine node import from %s" % path)
            return
        mc.sets(sels, fe=sg_node[0])
        maya_utils.delete_unused_nodes()
