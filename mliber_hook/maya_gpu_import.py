# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.maya_libs.maya_objects import MayaGpuCache


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)
        self.maya_object = MayaGpuCache(self.path)

    def execute(self, *args, **kwargs):
        gpu_shape_name = "%sGpuShape" % self.asset_name
        gpu_name = "%s_gpu" % self.asset_name
        return self.maya_object.import_in(gpu_shape_name, gpu_name)
