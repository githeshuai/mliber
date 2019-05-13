# -*- coding:utf-8 -*-
from image_converter import ImageConverter
from sequence_converter import SequenceConverter
from video_converter import VideoConverter


class SequenceConverterFactory(object):
    def __init__(self, typ):
        """
        :param typ: <str>
        """
        self.typ = typ

    def create(self, src, dst):
        """
        转换
        :return:
        """
        if self.typ == "image":
            instance = ImageConverter(src, dst)
        elif self.typ == "sequence":
            instance = SequenceConverter(src, dst)
        elif self.typ == "video":
            instance = VideoConverter(src, dst)
        else:
            return
        return instance
