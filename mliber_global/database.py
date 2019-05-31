# -*- coding:utf-8 -*-
import mliber_global


def database():
    """
    get global library
    :return:
    """
    return mliber_global.app().value("mliber_database")

