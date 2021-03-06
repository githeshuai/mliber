# -*- coding:utf-8 -*-
from Qt.QtWidgets import QToolButton


class IconWidget(QToolButton):
    def __init__(self, parent=None):
        super(IconWidget, self).__init__(parent)
        self.setStyleSheet("border: 0px solid; padding: 0px; background: transparent;")

    def mousePressEvent(self, event):
        """
        取消事件
        :param event:
        :return:
        """
        event.ignore()

    def set_icon(self, icon):
        """
        设置显示图片
        :return:
        """
        self.setIcon(icon)

    def set_icon_size(self, size):
        """
        set icon label size
        :param size:
        :return:
        """
        self.setIconSize(size)
        self.setFixedSize(size)
