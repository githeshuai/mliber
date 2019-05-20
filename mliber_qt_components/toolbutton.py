# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import QToolButton
from Qt.QtCore import QSize

from icon import Icon
from mliber_conf import mliber_config
import mliber_resource


class ToolButton(QToolButton):
    def __init__(self, parent=None):
        super(ToolButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStyleSheet("QToolButton{border: 0px; padding: 0px; background:transparent} "
                           "QToolButton::hover{background:transparent}")

    def set_size(self, width=30, height=30):
        """
        设置icon size
        :param width: <int>
        :param height: <int>
        :return:
        """
        self.setFixedSize(QSize(width, height))
        self.setIconSize(QSize(height*0.9, height*0.9))

    def set_icon(self, name, color=mliber_config.ICON_COLOR):
        """
        set icon
        :param name:
        :param color:
        :return:
        """
        if os.path.isfile(name):
            icon = Icon(name)
        else:
            icon = Icon(mliber_resource.icon(name))
        icon.set_color(color)
        self.setIcon(icon)

    def enterEvent(self, event):
        icon = Icon(self.icon())
        icon.set_color(mliber_config.ICON_HOVER_COLOR)
        self.setIcon(icon)

    def leaveEvent(self, *args, **kwargs):
        icon = Icon(self.icon())
        icon.set_color(mliber_config.ICON_COLOR)
        self.setIcon(icon)
