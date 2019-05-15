# -*- coding: utf-8 -*-
import os
import maya.mel as mel
from mliber_libs.maya_libs.maya_objects.maya_object import MayaObject
from mliber_libs.maya_libs.maya_utils import select_objects


class MayaFbx(MayaObject):
    plugin = "fbxmaya.mll"

    def __init__(self, path):
        """
        maya .obj
        Args:
            path: obj path
        Returns:

        """
        super(MayaFbx, self).__init__(path)

    def export(self, objects, *args, **kwargs):
        """
        export .fbx
        Returns:
        """
        if not objects:
            return
        select_objects(objects)
        dir_name = os.path.dirname(self.path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        mel.eval("FBXExport -f \"%s\" -s" % self.path)
        return self.path

    def import_in(self, *args, **kwargs):
        """
        import maya.fbx
        Returns:
        """
        mel.eval("FBXImport -file \"%s\";" % self.path)
