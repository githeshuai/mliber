# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
import maya.cmds as mc
from mliber_libs.maya_libs.maya_utils import load_plugin
from mliber_conf import mliber_config

TEXTURE_NODE_ATTR_DICT = mliber_config.TEXTURE_NODE_ATTR_DICT


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self, *args, **kwargs):
        if load_plugin("mtoa.mll"):
            light = "AR_ENV_DOME_LIGHTShape"
            if mc.objExists(light) and mc.nodeType(light) == "aiSkyDomeLight":
                file_node = mc.listConnections("%s.color" % light, s=1, d=0)[0]
            else:
                file_node = self.create_dome_light()
            attr = "%s.%s" % (file_node, TEXTURE_NODE_ATTR_DICT.get("file"))
            mc.setAttr(attr, self.path, type="string")
        else:
            self.append_error("Can not load plugin: mtoa.mll")

    @staticmethod
    def create_dome_light():
        node = mc.shadingNode("aiSkyDomeLight", asLight=1)
        node = mc.rename(node, "AR_ENV_DOME_LIGHT")
        child = mc.listRelatives(node, c=1)[0]
        child = mc.rename(child, "%sShape" % node)
        try:
            mc.setAttr("%s.camera" % child, 0)
        except:
            pass
        file_node = mc.shadingNode("file", asTexture=1, isColorManaged=1)
        mc.connectAttr("%s.outColor" % file_node, "%s.color" % child, f=1)
        return file_node
