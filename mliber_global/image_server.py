# -*- coding: utf-8 -*-
import mliber_global


def image_server():
    """
    get global library
    :return:
    """
    return mliber_global.app().value("mliber_image_server")
