# -*- coding:utf-8 -*-
from mliber_libs.os_libs.system import operation_system
from mliber_custom.public_path import PUBLIC_PATH


def public_dir():
    return PUBLIC_PATH.get(operation_system())


if __name__ == "__main__":
    from mliber_libs.os_libs.path import Path
    print Path(public_dir()).join("library/ss.png")
