# -*- coding:utf-8 -*-
import os
from mliber_conf import mliber_config
from image_converter import ImageConverter
from video_converter import VideoConverter


class Converter(object):
    def __init__(self, typ=None):
        """
        :param typ: <str>
        """
        self.typ = typ

    @staticmethod
    def get_thumbnail_type(thumbnail_files):
        """
        获取thumbnail类型，不同的类型，不同的处理方式
        :param thumbnail_files: <list> a file list.
        :return:
        """
        if not thumbnail_files:
            return
        if len(thumbnail_files) > 1:  # 图片或序列
            return "sequence"
        elif len(thumbnail_files) == 1:
            ext = os.path.splitext(thumbnail_files[0])[-1]
            if ext in mliber_config.VIDEO_EXT:
                return "video"
            return "image"

    def convert(self, src_files, dst_pattern):
        """
        main
        :param src_files: <list>
        :param dst_pattern: <str> /xxx/xxx/xxx.####.png
        :return:
        """
        if not src_files:
            return
        typ = self.typ if self.typ else self.get_thumbnail_type(src_files)
        if not typ:
            print "[MLIBER] warning: no type !"
            return
        if typ in ["image", "sequence"]:
            for index, src_file in enumerate(src_files):
                dst_file = dst_pattern.replace("####", str(index).zfill(4))
                ImageConverter(src_file, dst_file).convert()
        elif typ in ["video"]:
            src_file = src_files[0]
            dst_pattern = dst_pattern.replace("####", "%04d")
            VideoConverter(src_file, dst_pattern).convert()
