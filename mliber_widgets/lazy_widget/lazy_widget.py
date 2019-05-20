# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QCheckBox, QPushButton
from mliber_qt_components.thumbnail_widget import ThumbnailWidget
from mliber_qt_components.drag_file_widget import DragFileWidget


class LazyWidget(QWidget):
    def __init__(self, parent=None):
        super(LazyWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        # thumbnail widget
        self.thumbnail_widget = ThumbnailWidget(self)
        # drag file widget
        self.files_widget = DragFileWidget(self)
        # single or batch
        self.batch_check = QCheckBox(u"批量创建", self)
        # thumbnail check
        self.thumbnail_check = QCheckBox(u"从文件中生成缩略图", self)
        # create button
        self.create_button = QPushButton("Create", self)
        # add to main layout
        main_layout.addWidget(self.thumbnail_widget)
        main_layout.addWidget(self.files_widget)
        main_layout.addWidget(self.batch_check)
        main_layout.addWidget(self.thumbnail_check)
        main_layout.addWidget(self.create_button)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        lw = LazyWidget()
        lw.show()
