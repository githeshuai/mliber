#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-12-09 11:45
# Author    : Mr. He
# Version   :
# Usage     : 
# Notes     :

# Import built-in modules
import os
import sys
# Import third-party modules
import maya.cmds as mc
# Import local modules

mliber_dir = os.path.abspath(os.path.join(__file__, "../..")).replace("\\", "/")
sys.path.append(mliber_dir)
sys.path.append("{}/mliber_site_packages".format(mliber_dir))

from mliber_libs.megascans_libs.megascans_to_maya import MegascansToMaya
from mliber_api.maya_asset_maker import MayaAssetMaker


class JobMegascansToMaya(object):
    def __init__(self, database_name, library_id, category_id, asset_dir, types,
                 render_plugin_path, lod, resolution, renderer, export_texture,
                 overwrite, created_by):
        """
        :param database_name: <str> 配置文件中数据库的名字
        :param library_id: <str>
        :param category_id: <str>
        :param types: <str> element types
        :param asset_dir: <str> megascans asset dir
        :param render_plugin_path: <str> renderer .mll path
        :param lod: <str> LOD0 .....
        :param resolution: <str> 8K ....
        :param renderer: <str> Arnold....
        :param export_texture: <str> whether export texture
        :param overwrite: <str> whether overwrite exist asset
        :param created_by: <int> user id
        :return:
        """
        self.database_name = database_name
        self.library_id = int(library_id)
        self.category_id = int(category_id)
        self.asset_dir = asset_dir
        self.types = types.split(",")
        self.render_plugin_path = render_plugin_path
        self.lod = lod
        self.resolution = resolution
        self.renderer = renderer
        self.export_texture = bool(export_texture)
        self.overwrite = bool(overwrite)
        self.created_by = int(created_by)
        # load renderer plugin
        self.load_renderer_plugin()

    def load_renderer_plugin(self):
        """
        load renderer plugin
        :return:
        """
        mc.loadPlugin(self.render_plugin_path, quiet=1)

    @staticmethod
    def get_asset_model():
        """
        获取资产，在maya outline里
        :return:
        """
        all_assets = mc.ls(assemblies=1)
        exclude = ['persp', 'top', 'front', 'side']
        assets = list(set(all_assets) - set(exclude))
        if len(assets) > 1:
            group = mc.group(name="geometry", empty=1)
            mc.parent(assets, group)
            return group
        return assets

    def load_in_maya(self):
        """
        load in maya
        :return:
        """
        megascans_to_maya = MegascansToMaya(self.asset_dir, self.lod, self.resolution, self.renderer)
        asset = megascans_to_maya.asset
        self.asset_name = asset.name()
        self.thumbnail_files = asset.thumbnail()
        self.tag_names = asset.tags()
        megascans_to_maya.load_in_maya()

    def publish(self):
        """
        publish
        :return:
        """
        self.load_in_maya()
        print "Load in maya completed !"
        objects = self.get_asset_model()
        asset_maker = MayaAssetMaker(self.database_name, self.library_id, self.category_id, self.asset_name,
                                     objects, self.types, thumbnail_files=self.thumbnail_files,
                                     tag_names=self.tag_names, overwrite=self.overwrite, created_by=self.created_by,
                                     export_texture=self.export_texture, recover_texture=False)
        asset = asset_maker.make()
        print "Make asset completed !"
        return asset


if __name__ == "__main__":
    args = sys.argv[1:]
    print args
    megascans_to_maya = JobMegascansToMaya(*args)
    megascans_to_maya.publish()
