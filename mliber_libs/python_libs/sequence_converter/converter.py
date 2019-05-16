# -*- coding:utf-8 -*-
from image_converter import ImageConverter
from video_converter import VideoConverter


class Converter(object):
    def __init__(self, typ=None):
        """
        :param typ: <str>
        """
        self.typ = typ

    def convert(self, src_files, dst_pattern):
        """
        main
        :param src_files: <list>
        :param dst_pattern: <str> /xxx/xxx/xxx.####.png
        :return:
        """
        if not src_files:
            return
        if not self.typ:
            print "[MLIBER info]: no type !"
            return
        if self.typ in ["image", "sequence"]:
            for index, src_file in src_files:
                dst_file = dst_pattern.replace("####", str(index).zfill(4))
                ImageConverter(src_file, dst_file).convert()
        elif self.typ in ["video"]:
            src_file = src_files[0]
            dst_pattern = dst_pattern.replace("####", "%04d")
            VideoConverter(src_file, dst_pattern).convert()
