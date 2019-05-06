# -*- coding: utf-8 -*-
"""
选择 windows path/linux path/mac path
"""
from Qt.QtWidgets import QVBoxLayout, QWidget
from icon_line_edit import IconLineEdit
import mliber_resource


class PathWidget(QWidget):
    def __init__(self, parent=None):
        super(PathWidget, self).__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.windows_le = IconLineEdit(mliber_resource.icon_path("windows.png"), 30, 12, self)
        self.windows_le.setPlaceholderText("windows path")
        self.linux_le = IconLineEdit(mliber_resource.icon_path("linux.png"), 30, 12, self)
        self.linux_le.setPlaceholderText("linux path")
        self.mac_le = IconLineEdit(mliber_resource.icon_path("mac.png"), 30, 12, self)
        self.mac_le.setPlaceholderText("mac path")
        layout.addWidget(self.windows_le)
        layout.addWidget(self.linux_le)
        layout.addWidget(self.mac_le)

    def windows_path(self):
        """
        获取windows path
        :return:
        """
        return self.windows_le.text()

    def linux_path(self):
        """
        获取linux path
        :return:
        """
        return self.linux_le.text()

    def mac_path(self):
        """
        获取 mac path
        :return:
        """
        return self.mac_le.text()

    def set_windows_path(self, path):
        """
        set windows path
        :param path: <str>
        :return:
        """
        self.windows_le.setText(path)

    def set_linux_path(self, path):
        """
        set linux path
        :param path: <str>
        :return:
        """
        self.linux_le.setText(path)

    def set_mac_path(self, path):
        """
        set mac path
        :param path: <path>
        :return:
        """
        self.mac_le.setText(path)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        p = PathWidget()
        p.show()
