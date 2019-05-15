# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from mliber_libs.maya_libs.maya_utils import select_objects
from mliber_libs.maya_libs.maya_objects.maya_object import MayaObject


class MayaObj(MayaObject):
    plugin = "objExport.mll"

    def __init__(self, path):
        """
        maya .obj
        Args:
            path: obj path
        Returns:

        """
        super(MayaObj, self).__init__(path)

    def export(self, objects, start, end, padding=4, **kwargs):
        """
        export .obj
        start: start frame
        end: end frame
        padding:
        Returns:
        """
        if not objects:
            return
        select_objects(objects)
        parent_dir = os.path.dirname(self.path)
        if not os.path.isdir(parent_dir):
            os.makedirs(parent_dir)
        for i in range(start, end+1):
            mc.currentTime(i)
            prefix, suffix = os.path.splitext(self.path)
            new_path = "%s.%s%s" % (prefix, str(i).zfill(padding), suffix)
            mc.file(new_path, typ="OBJexport",
                    options="groups=0;ptgroups=0;materials=0;"
                            "smoothing=1;normals=1", pr=1, es=1, f=1)
        return self.path

    def import_in(self, *args, **kwargs):
        """
        import maya.obj
        Returns:
        """
        mc.file(self.path, i=1, type="OBJ", ignoreVersion=1, ra=1,
                mergeNamespacesOnClash=0, namespace=":", options="v=0", pr=1)
