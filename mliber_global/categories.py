# -*- coding:utf-8 -*-
import mliber_global


def categories():
    """
    get global library
    :return:
    """
    return mliber_global.app().value("mliber_categories")

