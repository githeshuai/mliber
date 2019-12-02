# -*- coding: utf-8 -*-
import maya.cmds as mc
from mliber_hook.base_hook import BaseHook
from mliber_libs.os_libs.path import Path
from mliber_conf import mliber_config


TEXTURE_NODE_ATTR_DICT = mliber_config.TEXTURE_NODE_ATTR_DICT


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self):
        selected = mc.ls(sl=1)
        if not selected:
            self._create_file_node()
        else:
            selected_texture_nodes = False
            for sel in selected:
                node_type = mc.nodeType(sel)
                if node_type in mliber_config.TEXTURE_NODE_ATTR_DICT:
                    selected_texture_nodes = True
                    attr = "%s.%s" % (sel, mliber_config.TEXTURE_NODE_ATTR_DICT.get(node_type))
                    mc.setAttr(attr, self.path, type="string")
            if not selected_texture_nodes:
                self._create_file_node()

    def _create_file_node(self):
        """
        创建file节点
        :return:
        """
        file_node = mc.shadingNode("file", asTexture=1, isColorManaged=1, name="file")
        attr = "%s.%s" % (file_node, TEXTURE_NODE_ATTR_DICT.get("file"))
        mc.setAttr(attr, self.path, type="string")
