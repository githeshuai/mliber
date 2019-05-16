# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from mliber_libs.maya_libs.maya_objects.maya_object import MayaObject


class MayaGpuCache(MayaObject):
    def __init__(self, path):
        """
        Args:
            path: <str> .abc file path
        Returns:
        """
        super(MayaGpuCache, self).__init__(path)
        self.plugin = "gpuCache.mll"

    def export(self, objects, start, end, save_multiple_files=True, **kwargs):
        """
        Args:
            objects: <str> maya object
            start: <int> start frame
            end: <int> end frame
            save_multiple_files:
        Returns:
        """
        if self.load_plugin():
            directory = os.path.dirname(self.path)
            filename = os.path.splitext(os.path.basename(self.path))[0]
            mc.gpuCache(objects, directory=directory, fileName=filename, optimize=1, writeMaterials=1, dataFormat="ogawa",
                        startTime=start, endTime=end, saveMultipleFiles=save_multiple_files)
            return self.path

    def import_in(self, gpu_name, node_name, *args, **kwargs):
        """
        :param gpu_name: gpu shape node name
        :param node_name: gpu node name
        :return:
        """
        gpu_node = mc.createNode("gpuCache", name=gpu_name)
        mc.setAttr("%s.cacheFileName" % gpu_node, self.path, type="string")
        parent_node = mc.listRelatives(gpu_node, parent=1)[0]
        final_name = mc.rename(parent_node, node_name)
        return final_name
