# -*- coding: utf-8 -*-
import mliber_global


def user():
    """
    get global library
    :return:
    """
    return mliber_global.app().value("mliber_user")
