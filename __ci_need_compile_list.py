# -*- coding: utf-8 -*-

import os


def get_dir_files(dir_path):
    files = os.listdir(dir_path)
    files = ["{}/{}".format(dir_path, file_item) for file_item in files]
    return files


compile_files = [
    "mliber_widgets/asset_widget/asset_delegate.py",
    "mliber_qt_components/image_sequence_widget.py",
    "mliber_libs/qt_libs/image_server.py",
    "mliber_widgets/tag_widget/tag_delegate.py",
    "mliber_widgets/library_manage/library_manage_delegate.py",
    "mliber_widgets/main_widget/main_widget.py"
]
for compile_file in compile_files:
    print(compile_file)
