# -*- coding:utf-8 -*-
from image_converter import ImageConverter
from mliber_site_packages.dayu_path import DayuPath
from mliber_libs.os_libs.path import Path


class SequenceConverter(object):
    def __init__(self, src_pattern, dst_pattern):
        """
        序列转换
        :param src_pattern: name.####.ext
        :param dst_pattern: name.####.ext
        """
        self.src = src_pattern
        self.dst = dst_pattern
        self.dayu_object = DayuPath(self.src)

    def frames(self):
        """
        获取序列的帧数
        :return: <list>
        """
        scan_gen = self.dayu_object.scan()
        scan_list = list(scan_gen)
        if scan_list:
            return scan_list[0].frames
        return []

    def file_list(self):
        """
        这种情况，self.src必须是带pattern的
        :return:
        """
        scan_gen = self.dayu_object.scan()
        scan_list = list(scan_gen)
        if scan_list:
            scan_object = scan_list[0]
            return [scan_object.restore_pattern(frame) for frame in scan_object.frames]
        return []

    def convert(self):
        """
        :return:
        """
        Path(self.dst).make_parent_dir()
        files = self.file_list()
        frames = self.frames()
        for index, frame in enumerate(frames):
            src_file = files[index]
            dst_file = self.dst.replace("####", str(frame+1).zfill(4))
            ImageConverter(src_file, dst_file).convert()


if __name__ == "__main__":
    src_pattern = "D:/textures/sequence/test/test.####.png"
    dst_pattern = "D:/textures/sequence/png/png.####.png"
    SequenceConverter(src_pattern, dst_pattern).convert()
