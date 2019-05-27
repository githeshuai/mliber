# -*- coding:utf-8 -*-
from mliber_hook.base_hook import BaseHook
import maya.cmds as mc
from mliber_libs.maya_libs.maya_utils import load_plugin
from mliber_conf import mliber_config

TEXTURE_NODE_ATTR_DICT = mliber_config.TEXTURE_NODE_ATTR_DICT


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name):
        super(Hook, self).__init__(path, objects, start, end, asset_name)

    def execute(self, *args, **kwargs):
        if load_plugin("redshift4maya.mll"):
            light = "RS_ENV_DOME_LIGHTShape"
            if mc.objExists(light) and mc.nodeType(light) == "RedshiftDomeLight":
                node = light
            else:
                node = self.create_dome_light()
            attr = "%s.%s" % (node, TEXTURE_NODE_ATTR_DICT.get("RedshiftDomeLight"))
            mc.setAttr(attr, self.path, type="string")
        else:
            self.append_error("Can not load plugin: redshift4maya.mll")

    @staticmethod
    def create_dome_light():
        node = mc.shadingNode("RedshiftDomeLight", asLight=1)
        node = mc.rename(node, "RS_ENV_DOME_LIGHT")
        child = mc.listRelatives(node, c=1)[0]
        child = mc.rename(child, "%sShape" % node)
        mc.setAttr("%s.background_enable" % child, 0)
        return child
