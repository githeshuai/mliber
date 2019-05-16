# -*- coding: utf-8 -*-
import maya.cmds as mc
from mliber_libs.os_libs.path import Path
from mliber_libs.maya_libs.maya_objects.maya_object import MayaObject
from mliber_libs.maya_libs.maya_utils import load_plugin, create_reference


class MayaAbc(MayaObject):
    def __init__(self, path):
        """
        Args:
            path: <str> .abc file path
        Returns:

        """
        super(MayaAbc, self).__init__(path)
        self.plugin = "AbcExport.mll"

    def export(self, objects, start=1, end=1, step=1, uv_write=True, strip_namespaces=True, data_format="ogawa",
               renderable_only=True, attribute=None, **kwargs):
        """
        export abc
        Args:
            objects: <list> maya objects
            start: <int>
            end: <int>
            step: <int>
            uv_write: <bool> whether write out uv
            strip_namespaces: <bool> whether strip namespace
            data_format: <str> abc format
            renderable_only: <bool> whether write out only renderable
            attribute: <list> attributes need to export.
        Returns:
        """
        root = objects
        if isinstance(root, basestring):
            root = [root]
        if isinstance(attribute, basestring):
            attribute = [attribute]
        tar_dir = Path(self.path).dirname()
        if not Path(tar_dir).isdir():
            Path(tar_dir).makedirs()
        if self.load_plugin():
            j_base_string = "-frameRange {start_frame} {end_frame} -step {step} -dataFormat {data_format} -worldSpace" \
                            " -writeVisibility -file {tar_path}"
            if uv_write:
                j_base_string += " -uvWrite"
            if renderable_only:
                j_base_string += " -renderableOnly"
            if strip_namespaces:
                j_base_string += " -stripNamespaces"
            if attribute:
                for attr in attribute:
                    j_base_string += " -u %s" % attr
            for r in root:
                j_base_string += " -root %s" % r
            j_string = j_base_string.format(start_frame=start, end_frame=end, step=step,
                                            data_format=data_format, tar_path=self.path)
            mc.AbcExport(j=j_string)
            return self.path

    def import_in(self, *args, **kwargs):
        """
        import in the abc file.
        Returns:
        """
        load_plugin(self.plugin)
        mc.AbcImport(self.path)

    def reference(self, namespace=":"):
        """
        reference in abc
        Args:
            namespace: <str> namespace
        Returns:
        """
        create_reference(self.path, namespace)
