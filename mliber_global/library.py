# -*- coding: utf-8 -*-
import mliber_global


def library():
    """
    get global library
    :return:
    """
    return mliber_global.app().value("mliber_library")
