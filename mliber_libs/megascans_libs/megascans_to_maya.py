#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-12-03 15:16
# Author    : Mr. He
# Version   :
# Usage     : 
# Notes     :

# Import built-in modules
import os
# Import third-party modules
import maya.cmds as mc
import maya.mel as mel
# Import local modules
from mliber_libs.megascans_libs.megascans_asset import MegascansAsset


class MegascansToMaya(object):
    def __init__(self, asset_dir, lod="LOD0", resolution="8K", renderer="Arnold"):
        self.asset_dir = asset_dir
        self.asset = MegascansAsset(self.asset_dir)
        self.asset_name = self.asset.name()
        self.asset_type = self.asset.type()
        self.lod = lod
        self.resolution = resolution
        self.renderer = renderer

    @staticmethod
    def _get_ext(file_path):
        """
        get ext of file
        :param file_path:
        :return:
        """
        return os.path.splitext(file_path)[-1][1:].lower()

    def import_meshes(self, mesh_files):
        """
        import meshes
        :param mesh_files: <list> mesh file paths
        :return: <list> list of maya object
        """
        mesh_list = list()
        if mesh_files:
            for mesh_file in mesh_files:
                mesh_ext = self._get_ext(mesh_file)
                if mesh_ext == "fbx":
                    mel.eval("FBXImport -file \"%s\";" % mesh_file)
                elif mesh_ext == "obj":
                    mc.file(mesh_file, i=1, type="OBJ", ignoreVersion=1, ra=1,
                            mergeNamespacesOnClash=0, namespace=":", options="v=0", pr=1)
            mesh_list = [mc.listRelatives(mesh, parent=1)[0] for mesh in mc.ls(type="mesh")]
        return mesh_list

    def import_texture(self):
        """
        创建材质球
        :return: <list> [[type, texture_node], ......]
        """
        type_textures = self.asset.type_textures(self.lod, self.resolution)
        texture_type_nodes = list()
        if type_textures:
            for texture_type, texture_path in type_textures:
                name = "{asset_name}_{texture_type}_file".format(asset_name=self.asset_name,
                                                                 texture_type=texture_type)
                texture_node = mc.shadingNode('file', asTexture=True, name=name)
                mc.setAttr("%s.ft" % texture_node, 2)
                mc.setAttr("%s.ftn" % texture_node, texture_path, type="string")
                if texture_type == "displacement":
                    exr_path = os.path.splitext(texture_path)[0] + ".exr"
                    if os.path.isfile(exr_path):
                        mc.setAttr("%s.ftn" % texture_node, exr_path, type="string")
                if self._get_ext(texture_path) == "exr":
                    mc.setAttr("%s.cs" % texture_node, "Raw", type="string")
                else:
                    if texture_type in ["albedo", "translucency", "specular"]:
                        mc.setAttr("%s.cs" % texture_node, "sRGB", type="string")
                    else:
                        mc.setAttr("%s.cs" % texture_node, "Raw", type="string")
                texture_type_nodes.append((texture_type, texture_node))
        return texture_type_nodes

    def arnold_setup(self, mesh_list, texture_type_nodes):
        """
        :param mesh_list: <list> list of maya object
        :param texture_type_nodes: <list> [[type, texture_node], ......]
        :return:
        """
        nodes = mc.allNodeTypes()
        if "aiStandardSurface" in nodes:
            material = mc.shadingNode('aiStandardSurface', asShader=True, name=self.asset_name + "_aiStandardSurface")
            shading_engine = mc.sets(r=True, nss=True, name=self.asset_name + "_shadingEngine")
            mc.connectAttr("%s.outColor" % material, "%s.surfaceShader" % shading_engine)
            texture_types = []
            for texture_type, texture_node in texture_type_nodes:
                texture_types.append(texture_type)
                if "normal" == texture_type:
                    normal = mc.shadingNode('aiNormalMap', asShader=True, name=self.asset_name + "_Normal")
                    mc.connectAttr("%s.outColor" % texture_node, "%s.input" % normal)
                    mc.connectAttr("%s.outValue" % normal, "%s.normalCamera" % material)
                elif "albedo" == texture_type:
                    mc.connectAttr("%s.outColor" % texture_node, "%s.baseColor" % material)
                elif "roughness" == texture_type:
                    ai_range = mc.shadingNode('aiRange', asShader=True, name=self.asset_name + "_aiRange")
                    mc.connectAttr("%s.outColor" % texture_node, "%s.input" % ai_range)
                    mc.connectAttr("%s.outColorR" % ai_range, "%s.specularRoughness" % material)
                    mc.setAttr("%s.alphaIsLuminance" % texture_node, 1)
                elif "displacement" == texture_type:
                    mc.connectAttr("%s.outColor" % texture_node, "%s.displacementShader" % shading_engine)
                    mc.setAttr("%s.alphaIsLuminance" % texture_node, 1)
                elif "metalness" == texture_type:
                    mc.connectAttr("%s.outAlpha" % texture_node, "%s.metalness" % material)
                    mc.setAttr("%s.alphaIsLuminance" % texture_node, 1)
                elif "translucency" == texture_type:
                    mc.connectAttr("%s.outColor" % texture_node, "%s.subsurfaceColor" % material)
                    mc.setAttr(material + ".subsurface", 1)
                    mc.setAttr(material + ".thinWalled", 1)
                elif "opacity" == texture_type:
                    mc.connectAttr("%s.outColor" % texture_node, "%s.opacity" % material)
                    mc.setAttr("%s.alphaIsLuminance" % texture_node, 1)
                    mc.setAttr(material + ".thinWalled", 1)
                elif "specular" == texture_type:
                    mc.connectAttr("%s.outColor" % texture_node, "%s.specularColor" % material)
            if mesh_list:
                mc.sets(mesh_list, e=1, forceElement=shading_engine)
            for mesh in mesh_list:
                shapes = mc.listRelatives(mesh, children=1, type="mesh")
                shape = shapes[0]
                if "displacement" in texture_types:
                    mc.setAttr("%s.aiSubdivType" % shape, 1)
                    mc.setAttr("%s.aiSubdivIterations" % shape, 3)
                    if self.asset_type in ["3dplant", "3d"]:
                        mc.setAttr("%s.aiDispHeight" % shape, 1)
                        mc.setAttr("%s.aiDispZeroValue" % shape, 0.5)
                    else:
                        mc.setAttr("%s.aiDispHeight" % shape, 10)
                        mc.setAttr("%s.aiDispZeroValue" % shape, 5)
                if "opacity" in texture_types:
                    mc.setAttr("%s.aiOpaque" % shape, 0)
                if "normal" not in texture_types:
                    mc.setAttr("%s.aiOpaque" % shape, 0)
                    mc.setAttr("%s.aiDispAutobump" % shape, 1)
        else:
            raise RuntimeError("Load arnold first.")

    def load_in_maya(self):
        """
        load to maya
        :return:
        """
        type_textures = self.asset.type_textures(self.lod, self.resolution)
        if not type_textures:
            print "No texture found in: %s" % self.asset_dir
            return
        texture_type_nodes = self.import_texture()
        mesh_files = self.asset.meshes(self.lod)
        mesh_list = self.import_meshes(mesh_files)
        if self.renderer == "Arnold":
            self.arnold_setup(mesh_list, texture_type_nodes)
