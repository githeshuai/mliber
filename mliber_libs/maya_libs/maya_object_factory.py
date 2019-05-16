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
    def __init__(self, typ):
        self.type = typ

    def create_instance(self, path):
        if self.type == "abc":
            instance = MayaAbc(path)
        elif self.type == "ass":
            instance = MayaArnoldProxy(path)
        elif self.type == "fbx":
            instance = MayaFbx(path)
        elif self.type in ["ma", "mb"]:
            instance = MayaFile(path)
        elif self.type == "gpu":
            instance = MayaGpuCache(path)
        elif self.type == "obj":
            instance = MayaObj(path)
        elif self.type == "rs":
            instance = MayaRedshiftProxy(path)
        elif self.type == "xarc":
            instance = MayaXgenProxy(path)
        else:
            print "[MLIBER] error: maya object type %s not supported." % self.type
            return
        return instance
