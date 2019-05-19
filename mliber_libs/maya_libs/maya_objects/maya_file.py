# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
import pymel.core as pm
from mliber_libs.maya_libs.maya_objects import MayaObject
from mliber_libs.maya_libs.maya_utils import get_file_type, select_objects, create_reference


class MayaFile(MayaObject):
    def __init__(self, path):
        """
        Args:
            path: <str> maya file path
        Returns:
        """
        super(MayaFile, self).__init__(path)
        self.file_type = get_file_type(self.path)

    def import_in(self, *args, **kwargs):
        """
        import maya file
        Returns:

        """
        mc.file(self.path, i=1, type=self.file_type, ignoreVersion=1, ra=1,
                mergeNamespacesOnClash=0, namespace=":", options="v=0", pr=1)

    def reference(self, namespace="liber", **kwargs):
        """
        reference
        Returns:
        """
        create_reference(self.path, namespace)

    def open(self, lnr=False, **kwargs):
        """
        open maya file
        Args:
            lnr: <bool> load no reference
        Returns:
        """
        pm.mel.eval('saveChanges("")')
        mc.file(self.path, open=1, f=1, loadNoReferences=lnr, ignoreVersion=1)

    def export(self, objects, pr_flag=False, **kwargs):
        """
        :param objects: 需要导出的物体
        :param pr_flag: if True: export still as reference, else: import
        :return:
        """
        if not objects:
            return
        select_objects(objects)
        parent_dir = os.path.dirname(self.path)
        if not os.path.isdir(parent_dir):
            os.makedirs(parent_dir)
        maya_type = get_file_type(self.path)
        mc.file(self.path, typ=maya_type, options="v=0", force=1, es=1, pr=pr_flag)
        return self.path

