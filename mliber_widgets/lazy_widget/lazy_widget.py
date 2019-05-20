# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout


class LazyWidget(QWidget):
    def __init__(self, parent=None):
        super(LazyWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        # single or batch
        top_layout = QHBoxLayout()
