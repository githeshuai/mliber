# -*- coding:utf-8 -*-
from PySide.QtGui import *
from PySide.QtCore import *


class MainWidgetUI(QDialog):
    def __init__(self, parent=None):
        super(MainWidgetUI, self).__init__(parent)
        title_layout = QHBoxLayout()