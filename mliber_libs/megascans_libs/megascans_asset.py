#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-12-03 12:29
# Author    : Mr. He
# Version   :
# Usage     : 
# Notes     :

# Import built-in modules
import os
import re
from glob import glob
# Import third-party modules

# Import local modules
from mliber_libs.os_libs.path import Path
from mliber_libs.python_libs.parser import Parser


class MegascansAsset(object):
    def __init__(self, asset_dir):
        self._asset_dir = asset_dir.replace("\\", "/")
        self._children = self._get_children_files()
        self._json_file = self._get_json_file()
        self._json_data = self._get_json_data()

    def type(self):
        """
        get asset type
        :return: <str> 3d or 3dPlant or brush or atlas
        """
        categories = self.categories()
        if categories:
            return categories[0]

    def _get_children_files(self):
        """
        get all children files
        :return: <list>
        """
        children = list()
        for root, dir_, files in os.walk(self._asset_dir):
            for each_file in files:
                children.append(Path(root).join(each_file))
        return children

    def _get_json_file(self):
        """
        get json file path
        :return:
        """
        json_files = glob("%s/*.json" % self._asset_dir)
        if len(json_files) == 1:
            return json_files[0]

    def _get_json_data(self):
        """
        get json file data
        :return: <dict>
        """
        if self._json_file:
            parser = Parser(self._json_file).parse()
            return parser.load()
        return {}

    def _get_file(self, fields, ext_list):
        """
        获取满足fields和ext list的path, 只取最先找到的一张
        :param fields: <list>
        :param ext_list: <list>
        :return: <str>
        """
        for each_file in self._children:
            file_basename = Path(each_file).basename()
            basename, ext = os.path.splitext(file_basename)
            if all([field in basename for field in fields]) and ext in ext_list:
                return each_file

    def _get_files(self, fields, ext_list):
        """
        get
        :param fields: <list>
        :param ext_list: <list>
        :return:
        """
        files = list()
        for each_file in self._children:
            file_basename = Path(each_file).basename()
            basename, ext = os.path.splitext(file_basename)
            if all([field in basename for field in fields]) and ext in ext_list:
                files.append(each_file)
        return files

    @staticmethod
    def _sort_field(field, filed_list):
        """
        sort field
        :param field: <str>
        :param filed_list: <list>
        :return:
        """
        if field in filed_list:
            index = filed_list.index(field)
            filed_list = filed_list[index:] + list(reversed(filed_list[:index]))
        return filed_list

    def asset_dir(self):
        """
        asset dir
        :return:
        """
        return self._asset_dir

    def thumbnail(self):
        """
        获取缩略图路径
        :return: <list>, 为什么要返回list,在入资产库的时候，需要的缩略图是一个列表。
        """
        files = Path(self._asset_dir).children()
        for f in files:
            if re.search("_[Tt]humb", f) or re.search("_[pP]review", f):
                return [Path(self._asset_dir).join(f)]
        return []

    def name(self):
        """
        get asset name
        :return:
        """
        # name = self._json_data.get("name")
        # if name:
        #     return name.replace(" ", "_")
        return Path(self._asset_dir).basename()

    def tags(self):
        """
        获取标签列表
        :return:
        """
        return self._json_data.get("tags", [])

    def categories(self):
        """
        获取分类
        :return:
        """
        return self._json_data.get("categories", [])

    def meshes(self, lod="LOD0"):
        """
        获取模型
        :return:
        """
        lod_fields = ["LOD0", "LOD1", "LOD2", "LOD3", "LOD4", "LOD5"]
        lod_fields = self._sort_field(lod, lod_fields)
        lod_fields.append("")
        ext_list = [".fbx", ".FBX", ".obj", ".OBJ"]
        for lod in lod_fields:
            meshes = self._get_files([lod], ext_list)
            if meshes:
                return meshes

    def textures(self, lod, resolution, texture_type):
        """
        获取贴图
        :param lod: <str> LOD
        :param resolution: <str> 1K , 2K ....
        :param texture_type: <str> Albedo....
        :return:
        """
        ext_list = [".JPG", ".jpg", ".png", ".PNG",  ".exr", ".EXR"]
        resolution_fields = ["1K", "2K", "4K", "8K"]
        resolution_fields = self._sort_field(resolution, resolution_fields)
        for resolution_field in resolution_fields:
            for lod_field in [lod, ""]:
                for type_field in [texture_type, texture_type.lower()]:
                    fields = (resolution_field, lod_field, resolution_field, type_field)
                    texture_path = self._get_file(fields, ext_list)
                    if texture_path:
                        return texture_path

    def type_textures(self, lod, resolution):
        """
        :param lod: <str>
        :param resolution: <str>
        :return: <list> [["normal", "/xxfsdf/sdf/asdf/sdf.ext"], ......]
        """
        type_textures = list()
        for texture_type in ["Normal", "Albedo", "Roughness", "Displacement", "Metalness", "Translucency", "Opacity",
                             "Bump", "Cavity", "fuzz", "Normalbump", "Specular", "Ao"]:
            texture_path = self.textures(lod, resolution, texture_type)
            if not texture_path:
                continue
            type_textures.append([texture_type.lower(), texture_path])
        return type_textures


if __name__ == "__main__":
    _dir = r"X:\work\ZCK\Megascans\Downloaded\3dplant\3d_Plant_shqke"
    mb = MegascansAsset(_dir)
    print mb.type_textures("LOD0", "Albedo")
