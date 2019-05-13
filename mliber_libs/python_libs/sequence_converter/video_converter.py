# -*- coding:utf-8 -*-
import subprocess
from mliber_libs.os_libs.path import Path


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
        cmd = "ffmpeg -i \"{0}\" -vf scale=256:ih/iw*256 -y \"{1}\" -hide_banner".format(self.src, self.dst)
        p = subprocess.Popen(cmd)
        p.wait()


if __name__ == "__main__":
    src = "D:/test.mp4"
    dst = "D:/textures/sequence/video_to_png/test.%04d.png"
    VideoConverter(src, dst).convert()
