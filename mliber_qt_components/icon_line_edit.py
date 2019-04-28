# -*- coding: utf-8 -*-
from Qt.QtWidgets import QApplication, QLineEdit
from Qt.QtGui import QPixmap, QPainter
from Qt.QtCore import Qt, QSize


class IconLineEdit(QLineEdit):
    def __init__(self, icon_path, height, font_size, parent=None):
        """
        QLineEdit with icon on left
        Args:
            icon_path: <str> icon file path
            height: <int> QLineEdit height
            font_size: <int> font size
            parent:
        Returns:
        """
        super(IconLineEdit, self).__init__(parent)
        self.setFixedHeight(height)
        pixmap = QPixmap(icon_path)
        pixmap_size = QSize(self.height()-2, self.height()-2)
        self.pixmap = pixmap.scaled(pixmap_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        style_sheet = "QLineEdit{padding-left: %dpx; height: %dpx;font-size: %dpx;" \
                      " background-color: rgb(200, 200, 200, 50);}" \
                      % (self.pixmap.width() + 5, height, font_size)
        self.setStyleSheet(style_sheet)

    def paintEvent(self, event):
        super(IconLineEdit, self).paintEvent(event)
        painter = QPainter(self)
        h = self.pixmap.height()
        right_border = 3
        painter.drawPixmap(right_border+2, (self.height()-h)/2, self.pixmap)


if __name__ == "__main__":
    app = QApplication([])
    le = IconLineEdit(r"E:\liber\liber_icons\password.png", 30, 15)
    le.show()
    app.exec_()
