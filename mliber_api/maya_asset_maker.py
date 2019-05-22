# -*- coding:utf-8 -*-
import logging
from asset_maker import AssetMaker
from mliber_api.api_utils import get_texture_dir
from mliber_libs.maya_libs.maya_utils import post_export_textures
from mliber_libs.maya_libs.maya_texture import MayaTexture


class MayaAssetMaker(AssetMaker):
    def __init__(self, database_name, library_id, category_id, asset_name, objects, types=list(), start=1, end=1,
                 thumbnail_files=list(), tag_names=list(), description="", overwrite=True, created_by=None,
                 export_texture=True, recover_texture=True):
        super(MayaAssetMaker, self).__init__(database_name, library_id, category_id, asset_name, objects, types, start,
                                             end, thumbnail_files, tag_names, description, overwrite, created_by)

        self.export_texture = export_texture
        self.recover_texture = recover_texture
        self._texture_info_dict = dict()

    def pre_create_elements(self):
        """
        在创建element之前先导出贴图
        :return:
        """
        if self.export_texture:
            try:
                texture_dir = get_texture_dir(self.asset_abs_dir)
                self._texture_info_dict = MayaTexture(self.objects).export(texture_dir)
                logging.info("[MLIBER] info: Export texture done.")
            except:pass
        return True

    def post_create_elements(self):
        """
        在创建element之后
        :return:
        """
        if self.export_texture and self.recover_texture:
            try:
                post_export_textures(self._texture_info_dict)
                logging.info("[MLIBER] info: Recover texture settings done.")
            except:
                logging.warning(u"[MLIBER] info: Texture can not be recovered.")
        return True
