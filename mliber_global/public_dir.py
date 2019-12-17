# -*- coding:utf-8 -*-
from mliber_libs.os_libs.system import operation_system
from mliber_custom import PUBLIC_PATH


def public_dir():
    return PUBLIC_PATH.get(operation_system())
