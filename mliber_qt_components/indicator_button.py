# -*- coding:utf-8 -*-
from Qt.QtWidgets import QPushButton
from Qt.QtCore import Qt
from mliber_conf import mliber_config


class IndicatorButton(QPushButton):
    def __init__(self, text, parent=None):
        super(IndicatorButton, self).__init__(text, parent)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("QPushButton{background: transparent; font-size: 13px; font: bold; color: #FFF; "
                           "Text-align:left; width: 60px; padding-left: 5px;}"
                           "QPushButton::hover{color: %s;}" % mliber_config.ACCENT_COLOR)
