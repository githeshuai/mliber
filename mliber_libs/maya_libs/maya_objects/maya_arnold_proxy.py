# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
from mliber_libs.maya_libs.maya_objects import MayaObject
from mliber_libs.maya_libs.maya_utils import get_frame_padding, load_plugin, select_objects


class MayaArnoldProxy(MayaObject):
    def __init__(self, path):
        """
        __init__ built in
        Args:
            path: when export, normal path
                  when import:  sequence pattern, eg: D:/test/test.####.ass
        Returns:
        """
        super(MayaArnoldProxy, self).__init__(path)
        self.plugin = "mtoa.mll"

    def get_ass_sequence_pattern(self, start, end):
        """
        Returns: <list> ass frame files
        """
        frame_padding = get_frame_padding()
        stem, ext = os.path.splitext(self.path)
        if start == end:
            frame = str(start).zfill(frame_padding)
        else:
            frame = "#"*frame_padding
        sequence_pattern = "{}.{}{}".format(stem, frame, ext)
        return sequence_pattern

    def pre_export_ass(self):
        """
        set format and load self.plugin
        Returns: <bool>
        """
        if self.load_plugin():
            mc.setAttr("defaultRenderGlobals.outFormatControl", 0)
            mc.setAttr("defaultRenderGlobals.animation", 1)
            mc.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
            mc.setAttr("defaultRenderGlobals.periodInExt", 1)
            return True
        return False

    def export(self, objects, start, end, *args, **kwargs):
        """
        Returns: <list> exported ass files.
        objects: <list> 需要导出的物体
        start: <int>
        end: <int>
        """
        if not objects:
            return
        select_objects(objects)
        if self.pre_export_ass():
            dir_name = os.path.dirname(self.path)
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
            mc.file(self.path, f=1,
                    options="-shadowLinks 1;-endFrame %s;-mask 255;-lightLinks 1;"
                            "-frameStep 1.0;-boundingBox;-startFrame %s" % (end, start),
                    typ="ASS Export", pr=1, es=1)
            return self.get_ass_sequence_pattern(start, end)

    def import_ass(self, ass_node_name):
        """
        import ass
        Args:
            ass_node_name:  ass node name in outliner
        Returns:
        """
        node = mc.createNode("aiStandIn", name="temp")
        parent_node = mc.listRelatives(node, parent=1)[0]
        parent_node = mc.rename(parent_node, ass_node_name)
        node = mc.rename(node, "%sShape" % parent_node)
        mc.setAttr("%s.dso" % node, self.path, type="string")
        return node

    def import_in(self, frames, ass_node_name="aiStandIn", **kwargs):
        """
        create arnold ass proxy
        Args:
            ass_node_name: <str> ass node name in outliner
            frames: <int> number of frames
        Returns:

        """
        if load_plugin(self.plugin):
            node = self.import_ass(ass_node_name)
            if frames > 1:
                mc.expression(s="{0}.frameNumber=(frame-1)%{1}+1".format(node, frames))
            return True
        else:
            print "[LIBER] warnning: Can not load plugin %s." % self.plugin
            return False
