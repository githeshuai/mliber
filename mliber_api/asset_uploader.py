# -*- coding:utf-8 -*-
import os
import logging
from dayu_path import DayuPath
from asset_maker import AssetMaker
from mliber_libs.os_libs.path import Path
from mliber_conf.element_type import ELEMENT_TYPE
from mliber_conf.templates import ELEMENT_PATH, ELEMENT_SEQUENCE_PATH


class AssetUploader(AssetMaker):
    def __init__(self, database_name, library_id, category_id, asset_name, objects, types=list(), start=1, end=1,
                 thumbnail_files=list(), tag_names=list(), description="", overwrite=True, created_by=None):
        super(AssetUploader, self).__init__(database_name, library_id, category_id, asset_name, objects, types, start,
                                            end, thumbnail_files, tag_names, description, overwrite, created_by)

    @staticmethod
    def _get_ext_from_file(source_file):
        """
        获取文件格式名字
        :param source_file:
        :return:
        """
        ext = os.path.splitext(source_file)[-1]
        ext = ext.split(".")[-1]
        return ext

    @staticmethod
    def _get_ext_from_files(source_files):
        """
        获取文件格式
        :param source_files: <list>
        :return:
        """
        ext_list = [os.path.splitext(source_file)[-1] for source_file in source_files]
        ext_list = list(set(ext_list))
        return ext_list

    def _get_element_type_from_file(self, source_file):
        """
        根据文件获取element type
        :param source_file: <str> a file path
        :return:
        """
        ext = self._get_ext_from_file(source_file)
        element_type = ext if ext in ELEMENT_TYPE else "source"
        return element_type

    def _get_element_type_from_files(self, source_files):
        """
        :param source_files: <str> a file list
        :return:
        """
        if len(source_files) < 1:
            return
        if len(source_files) == 1:
            source_file = source_files[0]
            return self._get_element_type_from_file(source_file)
        else:
            ext_list = self._get_ext_from_files(source_files)
            if len(ext_list) > 1:
                return
            return self._get_element_type_from_file(source_files[0])

    def _get_element_relative_path(self, source_files, asset_relative_dir, asset_name):
        """
        获取element的相对路径
        :param source_files:
        :return:
        """
        element_type = self._get_element_type_from_files(source_files)
        ext = self._get_ext_from_file(source_files[0])
        if len(source_files) == 1:
            element_relative_path = ELEMENT_PATH.format(asset_dir=asset_relative_dir, element_type=element_type,
                                                        asset_name=asset_name, ext="."+ext)
        else:
            element_relative_path = ELEMENT_SEQUENCE_PATH.format(asset_dir=asset_relative_dir,
                                                                 element_type=element_type,
                                                                 asset_name=asset_name, ext="."+ext)
        return element_relative_path

    def _copy_source_files(self, source_files, dst_path):
        """
        拷贝文件
        :param source_files: <list>
        :param dst_path: <str> 目标路径, 或者带####的pattern
        :return:
        """
        if len(source_files) == 1:
            Path(source_files[0]).copy_to(dst_path)
        else:
            # 判断是不是序列
            first_file = source_files[0]
            dayu_object = DayuPath(first_file)
            scan_gen = dayu_object.scan()
            scan_list = list(scan_gen)
            frames = scan_list[0].frames
            missing = scan_list[0].missing
            if frames:
                self.start = frames[0]
                self.end = frames[-1]
                if missing:
                    logging.warning(u"有丢失的帧：%s" % ",".join(missing))
                for index, frame in enumerate(frames):
                    dst_file = dst_path.replace("####", str(frame).zfill(4))
                    src_file = source_files[index]
                    if index >= len(source_files) - 1:  # dayu_path获取的是所有的帧数，如果只是序列的一部分，不判断会报错
                        break
                    Path(src_file).copy_to(dst_file)
            else:
                for index, src_file in enumerate(source_files):
                    dst_file = dst_path.replace("####", str(index).zfill(4))
                    Path(src_file).copy_to(dst_file)

    def create_elements(self):
        """
        继承自父类
        :return:
        """
        # 拷贝文件
        element_type = self._get_element_type_from_files(self.objects)
        element_relative_path = self._get_element_relative_path(self.objects, self.asset_relative_dir, self.asset_name)
        element_abs_path = element_relative_path.format(root=self.library.root_path())
        self._copy_source_files(self.objects, element_abs_path)
        logging.info("[MLIBER] info: Copy files done.")
        # 创建element
        element = self._create_element(self.db, element_type, element_relative_path)
        logging.info("[MLIBER] info: Create element done.")
        elements = [element]
        return elements

    def upload(self):
        """
        :return:
        """
        return self.make()
