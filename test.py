# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QApplication
from Qt.QtGui import QImage, QPalette, QBrush
from Qt.QtCore import Qt


class HasBackgroundWidget(QWidget):
    def __init__(self, image_path, parent=None):
        super(HasBackgroundWidget, self).__init__(parent)
        self.image_path = image_path
        self.set_background()

    def set_background(self):
        self.image = QImage()
        self.image.load(self.image_path)
        self.setAutoFillBackground(True)
        self.set_palette()

    def set_palette(self):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.image.scaled(self.width(), self.height(),
                                                                                   Qt.KeepAspectRatio,
                                                                                   Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.set_palette()


if __name__ == "__main__":
    app = QApplication([])
    widget = HasBackgroundWidget(r"D:\textures\seamless\3.jpg")
    widget.show()
    app.exec_()
