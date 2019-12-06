# -*- coding:utf-8 -*-
import os
import subprocess
from mliber_libs.python_libs.temp import Temporary
from mliber_libs.os_libs.path import Path
from mliber_custom import THUMBNAIL_SIZE


class ImageConverter(object):
    def __init__(self, src_path, dst_path):
        """
        图片转换
        :param src_path: <str>
        :param dst_path: <str>
        """
        self.src = src_path
        self.dst = dst_path

    @staticmethod
    def resize_image_with_oiio(src_image_path, dst_image_path, ratio=0.5):
        """
        在本软件中，用来将HDR转换成exr
        Args:
            src_image_path: <str>
            dst_image_path: <str>
            ratio:
        Returns:
        """
        from mliber_site_packages.OpenImageIO import OpenImageIO as oiio
        dst_image_dir = os.path.dirname(dst_image_path)
        if not os.path.isdir(dst_image_dir):
            os.makedirs(dst_image_dir)
        input_image = oiio.ImageInput.open(src_image_path)
        if not input_image:
            print 'Could not open %s "' % input_image
            print "\tError: ", oiio.geterror()
            return
        image_spec = input_image.spec()
        bit = image_spec.format
        channel_num = image_spec.nchannels
        buf_src = oiio.ImageBuf(src_image_path)
        obj = oiio.ImageSpec(int(image_spec.width * ratio), int(image_spec.height * ratio), channel_num, bit)
        # obj.attribute("tiff.ColorSpace", "sRGB")
        dst = oiio.ImageBuf(obj)
        oiio.ImageBufAlgo.resize(dst, buf_src)
        dst.write(dst_image_path)
        dst.clear()
        buf_src.clear()
        input_image.close()

    def convert(self):
        """
        主函数
        :return:
        """
        Path(self.dst).make_parent_dir()
        ext = os.path.splitext(self.src)[-1]
        if ext in [".hdr"]:
            self.convert_hdr()
        elif ext in [".exr"]:
            self.convert_exr()
        else:
            self.convert_image()

    def convert_image(self):
        """
        转换普通的贴图
        :return:
        """
        cmd = "ffmpeg -i \"{input}\" -vf scale={thumbnail_size}:ih/iw*{thumbnail_size} -y \"{output}\"".\
            format(input=self.src, thumbnail_size=THUMBNAIL_SIZE, output=self.dst)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()

    def convert_exr(self):
        """
        转换exr
        :return:
        """
        cmd = "ffmpeg -apply_trc iec61966_2_1 -i \"{input}\" -vf scale={thumbnail_size}:ih/iw*{thumbnail_size} -y \"{output}\"".\
            format(input=self.src, thumbnail_size=THUMBNAIL_SIZE, output=self.dst)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()

    def convert_hdr(self):
        """
        转换HDR
        :return:
        """
        with Temporary(suffix=".exr", mode="mktemp") as tmp:
            self.resize_image_with_oiio(self.src, tmp)
            ImageConverter(tmp, self.dst).convert()


if __name__ == "__main__":
    src = r"X:\work\ZCK\Megascans\Downloaded\brush\brushes_prints_sb0rdiop\sb0rdiop_Preview.png"
    dst = "D:/test.jpg"
    ImageConverter(src, dst).convert()
