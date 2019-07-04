# -*- coding:utf-8 -*-
import subprocess
from mliber_libs.os_libs.path import Path
from mliber_custom import THUMBNAIL_SIZE


class VideoConverter(object):
    def __init__(self, src_path, dst_pattern):
        """
        built in
        :param src_path: <str> video path
        :param dst_pattern: <str> 必须带%04d
        """
        self.src = src_path
        self.dst = dst_pattern

    def convert(self):
        """
        :return:
        """
        Path(self.dst).make_parent_dir()
        cmd = "ffmpeg -i \"{input}\" -vf scale={thumbnail_size}:ih/iw*{thumbnail_size} -y \"{output}\" -hide_banner"\
            .format(input=self.src, thumbnail_size=THUMBNAIL_SIZE, output=self.dst)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()


if __name__ == "__main__":
    src = "D:/test.mp4"
    dst = "D:/textures/sequence/video_to_png/test.%04d.png"
    VideoConverter(src, dst).convert()
