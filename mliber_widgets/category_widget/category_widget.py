# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from category_tree import CategoryTree


class CategoryWidget(QWidget):
    def __init__(self, parent=None):
        super(CategoryWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.category_tree = CategoryTree(self)
        main_layout.addWidget(self.category_tree)

