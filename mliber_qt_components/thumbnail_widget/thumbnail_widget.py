# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout
from Qt.QtCore import Qt
from mliber_qt_components.drag_file_widget import DragFileWidget
from mliber_qt_components.screen_shot import ScreenShotWidget
import mliber_resource
from mliber_libs.python_libs.sequence_converter import Converter


class ThumbnailWidget(QWidget):
    def __init__(self, parent=None):
        super(ThumbnailWidget, self).__init__(parent)
        self._current_index = 0
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_widget = QTabWidget(self)
        # screen shot widget
        screen_widget = QWidget(self)
        screen_layout = QHBoxLayout(screen_widget)
        screen_layout.setAlignment(Qt.AlignCenter)
        self.screen_shot_widget = ScreenShotWidget(self)
        self.screen_shot_widget.setFixedSize(180, 180)
        screen_layout.addWidget(self.screen_shot_widget)
        # drag file widget
        self.file_widget = DragFileWidget(self)
        # add to tab widget
        self.tab_widget.addTab(screen_widget, mliber_resource.icon("screen.png"), "screen shot")
        self.tab_widget.addTab(self.file_widget, mliber_resource.icon("picture.png"), "local file")
        # add to main layout
        main_layout.addWidget(self.tab_widget)

    def current_type(self):
        """
        获取当前type
        :return:
        """
        current_index = self.tab_widget.currentIndex()
        if current_index == 0:
            return "screen"
        return "files"

    def files(self):
        """
        获取当前thumbnail files
        :return:
        """
        current_type = self.current_type()
        if current_type == "screen":
            thumbnail_path = self.screen_shot_widget.get_thumbnail_path()
            if thumbnail_path:
                return [thumbnail_path]
            return []
        else:
            return self.file_widget.item_texts()

    def convert_to(self, dst_pattern):
        """
        转换缩略图
        :param dst_pattern: /xxx/xxx/xxx.####.png
        :return:
        """
        files = self.files()
        if not files:
            return
        converter = Converter(self.current_type())
        converter.convert(files, dst_pattern)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = ThumbnailWidget()
        tw.show()
