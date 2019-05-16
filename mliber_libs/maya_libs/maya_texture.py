# -*- coding: utf-8 -*-
import os
import re
import maya.cmds as mc
from mliber_conf import mliber_config
from mliber_libs.os_libs.file_opt import copy_file


TEXTURE_NODE_ATTR_DICT = mliber_config.TEXTURE_NODE_ATTR_DICT
COLOR_SPACE_ATTR_DICT = mliber_config.COLOR_SPACE_ATTR_DICT


class MayaTexture(object):
    def __init__(self, objects):
        """
        Args:
            objects: <list> maya objects
        Returns:
        """
        if isinstance(objects, basestring):
            objects = [objects]
        self.objects = objects

    def sg_nodes(self):
        """
        get shading group of selected
        Returns:

        """
        sg_nodes = list()
        for sel in self.objects:
            if mc.nodeType(sel) in ["transform"]:
                shape = mc.listRelatives(sel, ad=1, c=1, fullPath=1, type="mesh")
            else:
                shape = sel
            sg_node = mc.listConnections(shape, s=0, d=1, type="shadingEngine")
            if not sg_node:
                continue
            sg_nodes.extend(sg_node)
        sg_nodes = list(set(sg_nodes))
        return sg_nodes

    @staticmethod
    def get_history_nodes(sg_node):
        """
        get all history node of sg node
        Args:
            sg_node: <str> sg node
        Returns: <list>
        """
        history_nodes = mc.listHistory(sg_node, ac=1)
        history_nodes = list(set(history_nodes))
        return history_nodes

    def get_texture_nodes_of_sg(self, sg_node):
        """
        get texture nodes of one sg node
        Args:
            sg_node: <str> sg node
        Returns: <list>
        """
        history_nodes = self.get_history_nodes(sg_node)
        texture_nodes = list()
        for typ in TEXTURE_NODE_ATTR_DICT.keys():
            try:
                texture_node = mc.ls(history_nodes, type=typ)
                if not texture_node:
                    continue
                texture_nodes.extend(texture_node)
            except:pass
        return texture_nodes

    def texture_nodes(self):
        """
        get all texture nodes of objects
        Returns:
        """
        sg_nodes = self.sg_nodes()
        all_texture_nodes = list()
        for sg_node in sg_nodes:
            texture_nodes = self.get_texture_nodes_of_sg(sg_node)
            all_texture_nodes.extend(texture_nodes)
        texture_nodes = list(set(all_texture_nodes))
        return texture_nodes

    @staticmethod
    def get_texture_abs_path(texture):
        """
        get abs path of texture, for convert <UDIM> to real path
        Args:
            texture:

        Returns:

        """
        real_texture = list()
        if not texture:
            return []
        texture = texture.replace("\\", "/")
        if texture.startswith("$"):
            _list = texture.split("/")
            prefix = _list[0]
            env = prefix.split("$")[-1]
            env = env.strip("{").strip("}")
            suffix = "/".join(_list[1:])
            env_path = os.environ.get(env)
            if not env_path:
                return []
            texture = "{0}/{1}".format(env_path, suffix)
        if "<udim>" in texture or "<UDIM>" in texture:
            texture_dir, texture_base_name = os.path.split(texture)
            pattern = texture_base_name.replace("<udim>", "\d{4}")
            pattern = pattern.replace("<UDIM>", "\d{4}")
            if os.path.isdir(texture_dir):
                for i in os.listdir(texture_dir):
                    if re.match(pattern, i):
                        full_name = "%s/%s" % (texture_dir, i)
                        full_name = full_name.replace("\\", "/")
                        real_texture.append(full_name)
        elif os.path.isfile(texture):
            real_texture.append(texture)
        else:
            print "[MAYATEXTURE] warning: %s is not an exist file." % texture
        return real_texture

    def export(self, texture_dir):
        """
        export textures to target directory
        Args:
            texture_dir: <str> target dir
        Returns:<dict> attr: value

        """
        texture_nodes = self.texture_nodes()
        if not texture_nodes:
            return
        temp_dict = dict()
        for node in texture_nodes:
            node_type = mc.nodeType(node)
            attr = "%s.%s" % (node, TEXTURE_NODE_ATTR_DICT.get(node_type))
            color_space_attr = COLOR_SPACE_ATTR_DICT.get(node_type)
            cs_attr = "%s.%s" % (node, color_space_attr) if color_space_attr else None
            temp_dict[attr] = mc.getAttr(attr)
            if cs_attr:
                temp_dict[cs_attr] = mc.getAttr(cs_attr)
        for node in texture_nodes:
            try:
                self.export_texture(node, texture_dir, True)
            except Exception as e:
                print "[MAYATEXTURE] error: %s" % str(e)
        return temp_dict

    def export_texture(self, node, tex_dir, change_file_texture_name):
        """
        export single texture node textures
        Args:
            node: <str> texture node
            tex_dir: <str> target directory
            change_file_texture_name: <bool>
                when true: after export change the texture node's value
        Returns:

        """
        node_type = mc.nodeType(node)
        attr = "%s.%s" % (node, TEXTURE_NODE_ATTR_DICT.get(node_type))
        texture = mc.getAttr(attr)
        if node_type == "file":
            texture = mc.getAttr("%s.computedFileTextureNamePattern" % node)
        if not texture:
            return
        texture = texture.replace("\\", "/")
        if not os.path.splitdrive(texture)[0]:
            texture = "%s%s" % (mc.workspace(q=1, rootDirectory=1, fullName=1), texture)
        real_path = self.get_texture_abs_path(texture)
        if not real_path:
            return
        for each_path in real_path:
            base_name = os.path.basename(each_path)
            new_path = "%s/%s" % (tex_dir, base_name)
            if copy_file(each_path, new_path):
                print "[MAYATEXTURE] info: Copy %s >> %s" % (each_path, new_path)
        if change_file_texture_name:
            texture_base_name = os.path.basename(texture)
            new_texture_path = "%s/%s" % (tex_dir, texture_base_name)
            color_space_attr = COLOR_SPACE_ATTR_DICT.get(node_type)
            cs_attr = "%s.%s" % (node, color_space_attr) if color_space_attr else None
            cs_value = mc.getAttr(cs_attr) if cs_attr else None
            mc.setAttr(attr, new_texture_path, type="string")
            if cs_attr and cs_value:
                mc.setAttr(cs_attr, cs_value, type="string")
