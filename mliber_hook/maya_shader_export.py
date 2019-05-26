# -*- coding: utf-8 -*-
import maya.cmds as mc
from mliber_libs.os_libs.path import Path
from mliber_hook.base_hook import BaseHook
from mliber_libs.maya_libs.maya_texture import MayaTexture
from mliber_libs.maya_libs import maya_utils


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name):
        super(Hook, self).__init__(path, objects, start, end, asset_name)
        self.maya_texture = MayaTexture(self.objects)

    def execute(self, *args, **kwargs):
        # 获取选择物体的sg节点，导出贴图，然后导出sg节点
        sg_nodes = self.maya_texture.sg_nodes()
        parent_dir = Path(self.path).ancestor(2)
        texture_dir = Path(parent_dir).join("texture")
        # 导出贴图
        temp_dict = self.maya_texture.export(texture_dir)
        # 导出sg node
        mc.select(sg_nodes, ne=1, r=1)
        maya_utils.export_selected(self.path, False)
        # 还原贴图
        maya_utils.post_export_textures(temp_dict)
        mc.select(self.objects, r=1)
        return self.path
