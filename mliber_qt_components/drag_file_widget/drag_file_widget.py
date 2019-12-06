# -*- coding: utf-8 -*-
from Qt.QtWidgets import QStackedLayout, QWidget
from file_list_widget import FileListWidget
from press_label import PressLabel


class DragFileWidget(QWidget):
    def __init__(self, parent=None):
        super(DragFileWidget, self).__init__(parent)
        self.resize(200, 200)
        self.stacked_layout = QStackedLayout(self)
        self.press_label = PressLabel(self)
        self.file_list = FileListWidget(self)
        self.stacked_layout.addWidget(self.press_label)
        self.stacked_layout.addWidget(self.file_list)
        self._set_signals()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.press_label.clicked.connect(self.add_file_to_list)

    def add_file_to_list(self, file_list):
        """
        添加文件
        :param file_list:
        :return:
        """
        if not file_list:
            return
        for f in file_list:
            self.file_list.add_file_item(f)
        self.stacked_layout.setCurrentIndex(1)

    def item_texts(self):
        """
        获取所有item 的text
        :return:
        """
        return self.file_list.all_items_text()

    def clear(self):
        """
        清空
        :return:
        """
        self.file_list.clear()

    def set_filter(self, filter_list):
        """
        只显示固定格式的文件
        :param filter_list: <list>
        :return:
        """
        self.file_list.set_filter(filter_list)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        dfw = DragFileWidget()
        dfw.show()
