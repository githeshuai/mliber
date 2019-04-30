# -*- coding:utf-8 -*-
from PySide.QtWidgets import *
from PySide.QtGui import *
from PySide.QtCore import *


class CellLibrary(QWidget):
    def __init__(self, parent=None):
        super(CellLibrary, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        self.icon_label = QLabel(self)

