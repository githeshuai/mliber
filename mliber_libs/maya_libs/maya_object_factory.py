# -*- coding:utf-8 -*-
from mliber_libs.maya_libs.maya_objects.maya_abc import MayaAbc
from mliber_libs.maya_libs.maya_objects.maya_arnold_proxy import MayaArnoldProxy
from mliber_libs.maya_libs.maya_objects.maya_fbx import MayaFbx
from mliber_libs.maya_libs.maya_objects.maya_file import MayaFile
from mliber_libs.maya_libs.maya_objects.maya_gpucache import MayaGpuCache
from mliber_libs.maya_libs.maya_objects.maya_obj import MayaObj
from mliber_libs.maya_libs.maya_objects.maya_redshift_proxy import MayaRedshiftProxy
from mliber_libs.maya_libs.maya_objects.maya_xgen_proxy import MayaXgenProxy


class MayaObjectFactory(object):
    def __init__(self, typ, path):
        self.type = typ
        self.path = path

    def create_instance(self):
        if self.type == "abc":
            instance = MayaAbc(self.path)
        elif self.type == "ass":
            instance = MayaArnoldProxy(self.path)
        elif self.type == "fbx":
            instance = MayaFbx(self.path)
        elif self.type in ["ma", "mb"]:
            instance = MayaFile(self.path)
        elif self.type == "gpu":
            instance = MayaGpuCache(self.path)
        elif self.type == "obj":
            instance = MayaObj(self.path)
        elif self.type == "rs":
            instance = MayaRedshiftProxy(self.path)
        elif self.type == "xgen":
            instance = MayaXgenProxy(self.path)
        else:
            print "[MLIBER] error: maya object type %s not supported." % self.type
            return
        return instance
