# -*- coding:utf-8 -*-
from Qt.QtWidgets import QPushButton
from Qt.QtCore import Qt, QSize
import mliber_resource


class TitleWidget(QPushButton):
    def __init__(self, parent=None):
        super(TitleWidget, self).__init__(parent)
        self.setText("    M-Liber")
        self.setMinimumHeight(50)
        self.setIcon(mliber_resource.icon("logo.png"))
        self.setIconSize(QSize(20, 20))
        self.setStyleSheet("background: #2d2f37; padding: 0px; color: #FFF; font: bold; font-size: 16px;")