# -*- coding: utf-8 -*-
from Qt.QtGui import QIcon, QPainter
from Qt.QtCore import QSize


class Icon(QIcon):
    def __init__(self, parent=None):
        super(Icon, self).__init__(parent)

    def set_color(self, color, size=None):
        size = size or self.actualSize(QSize(256, 256))
        pixmap = self.pixmap(size)
        if not self.isNull():
            painter = QPainter(pixmap)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.setBrush(color)
            painter.setPen(color)
            painter.drawRect(pixmap.rect())
            painter.end()
        icon = QIcon(pixmap)
        self.swap(icon)
