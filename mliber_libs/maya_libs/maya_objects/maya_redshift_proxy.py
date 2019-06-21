# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from mliber_libs.maya_libs.maya_objects import MayaObject
from mliber_libs.maya_libs.maya_utils import load_plugin, select_objects


class MayaRedshiftProxy(MayaObject):
    
    def __init__(self, path):
        """
        __init__ built in
        Args:
            path: when export, normal path
                  when import:  sequence pattern, eg: D:/test/test.####.rs
        Returns:
        """
        super(MayaRedshiftProxy, self).__init__(path)
        self.plugin = "redshift4maya.mll"

    def get_rs_sequence_pattern(self, start, end):
        """
        Returns: <list> ass frame files
        """
        frame_padding = 4
        stem, ext = os.path.splitext(self.path)
        if start == end:
            sequence_pattern = self.path
        else:
            frame = "#"*frame_padding
            sequence_pattern = "{}.{}{}".format(stem, frame, ext)
        return sequence_pattern

    def export(self, objects, start, end, *args, **kwargs):
        """
        export redshift proxy
        Returns:
        """
        if not objects:
            return
        if self.load_plugin():
            select_objects(objects)
            dir_name = os.path.dirname(self.path)
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
            mc.file(self.path, pr=1, es=1, force=1, typ="Redshift Proxy",
                    options="startFrame=%s;endFrame=%s;frameStep=1;exportConnectivity=0;" % (start, end))
            return self.get_rs_sequence_pattern(start, end)

    def import_rs(self, rs_node_name):
        """
        Args:
            rs_node_name: <str> rs proxy node in maya outliner
        Returns:
        """
        rs_proxy_node = mc.createNode("RedshiftProxyMesh", name=rs_node_name)
        rs_proxy_placeholder_shape = mc.createNode("mesh", name="temp")
        transform = mc.listRelatives(rs_proxy_placeholder_shape, parent=1)[0]
        transform = mc.rename(transform, os.path.basename(self.path).split(".")[0])
        rs_proxy_placeholder_shape = mc.rename(rs_proxy_placeholder_shape, "%sShape" % transform)
        mc.connectAttr("%s.outMesh" % rs_proxy_node, "%s.inMesh" % rs_proxy_placeholder_shape, f=1)
        mc.setAttr("%s.fn" % rs_proxy_node, self.path, type="string")
        if mc.objExists("initialShadingGroup"):
            mc.sets(rs_proxy_placeholder_shape, fe="initialShadingGroup")
        return rs_proxy_node

    def import_in(self, frames, rs_node_name="redshiftProxy", **kwargs):
        """
        create rs proxy
        Args:
            frames: <int>
            rs_node_name: redshift node name
        Returns:<bool>

        """
        if load_plugin(self.plugin):
            node = self.import_rs(rs_node_name)
            if frames > 1:
                mc.setAttr("%s.useFrameExtension" % node, True)
                exp = mc.createNode("expression", name="expression")
                mc.connectAttr("%s.out[0]" % exp, "%s.frameExtension" % node, f=1)
                mc.expression(exp, e=1, s="{0}.frameExtension=(frame-1)%{1}+1".format(node, frames), ae=1, uc="all")
            return True
        print "[LIBER] warnning: Can not load plugin %s." % self.plugin
        return False
