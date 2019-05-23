# -*- coding: utf-8 -*-
from Qt.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSizeGrip, QLabel, QToolButton
from Qt.QtGui import QBrush, QPalette, QImage
from Qt.QtCore import Qt, QSize

import mliber_resource


class FramelessWidget(QDialog):
    def __init__(self, parent=None):
        super(FramelessWidget, self).__init__(parent)
        self.setMinimumHeight(50)
        self.is_maximum = False
        self.__central_widget = None
        self.drag_position = None
        self.has_background = False
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout = QHBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        # title layout
        title_layout = self.create_title_layout()
        main_layout.addLayout(title_layout)
        main_layout.addLayout(self.central_layout)
        # size grip
        size_grip = QSizeGrip(self)
        main_layout.addWidget(size_grip, 0, Qt.AlignBottom | Qt.AlignRight)
        main_layout.setSpacing(0)
        # build connections
        self.build_connections()

    def create_title_layout(self):
        """
        create top tilte layout
        Returns:QHBoxLayout
        """
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 1, 0, 5)
        self.icon_label = QLabel(self)
        self.icon_label.setStyleSheet("background: transparent;")
        self.title_label = QLabel(self)
        self.title_label.setStyleSheet("background: transparent;")
        self.minimum_btn = QToolButton(self)
        self.minimum_btn.setIcon(mliber_resource.icon("minus.png"))
        self.minimum_btn.setStyleSheet("QToolButton{background-color: rgb(255, 255, 255, 10); "
                                       "padding:0px; border: 0px solid;}"
                                       "QToolButton::hover{background-color: #707070}")
        self.maximum_btn = QToolButton(self)
        self.maximum_btn.setIcon(mliber_resource.icon("max.png"))
        self.maximum_btn.setStyleSheet("QToolButton{background-color: rgb(255, 255, 255, 10);"
                                       "padding:0px; border: 0px solid;} "
                                       "QToolButton::hover{background-color: #707070}")
        self.close_btn = QToolButton(self)
        self.close_btn.setIcon(mliber_resource.icon("close.png"))
        self.close_btn.setStyleSheet("QToolButton{background-color: rgb(255, 255, 255, 10); "
                                     "padding:0px; border: 0px solid;}"
                                     "QToolButton::hover{background-color: #D50000}")
        title_layout.addWidget(self.icon_label)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.minimum_btn)
        title_layout.addWidget(self.maximum_btn)
        title_layout.addWidget(self.close_btn)
        return title_layout

    def build_connections(self):
        """
        build connections
        Returns:
        """
        self.minimum_btn.clicked.connect(self.minimum)
        self.maximum_btn.clicked.connect(self.maximum)
        self.close_btn.clicked.connect(self.close)

    def set_window_flag(self, flag):
        """
        set window flat
        Args:
            flag: <str> if dialog hide maximum button
        Returns:
        """
        if flag == "dialog":
            self.maximum_btn.hide()
        else:
            self.maximum_btn.show()

    def set_window_title(self, title):
        """
        set window title
        Args:
            title: <str>
        Returns:
        """
        self.title_label.setText(title)

    def set_window_icon(self, pixmap):
        """
        set window icon
        Args:
            pixmap: QPixmap
        Returns:

        """
        self.icon_label.setMaximumSize(QSize(22, 22))
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setScaledContents(True)

    def set_window_modality(self):
        """
        模态显示
        :return:
        """
        self.setWindowModality(Qt.WindowModal)

    def set_central_widget(self, widget):
        """
        add central widget
        Args:
            widget: QWidget
        Returns:

        """
        self.__central_widget = widget
        self.central_layout.addWidget(widget)

    def central_widget(self):
        """
        get central widget
        Returns:
        """
        return self.__central_widget

    def minimum(self):
        """
        最小化
        Returns:
        """
        self.showMinimized()

    def maximum(self):
        """
        最大化
        Returns:
        """
        if self.is_maximum:
            self.maximum_btn.setIcon(mliber_resource.icon("max.png"))
            self.showNormal()
        else:
            self.maximum_btn.setIcon(mliber_resource.icon("normal.png"))
            self.showMaximized()
        self.is_maximum = not self.is_maximum

    def set_background_color(self, image_path):
        """
        set background color
        Args:
            image_path: <str> an image path
        Returns:
        """
        self.image = QImage()
        self.image.load(image_path)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background,
                         QBrush(self.image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)
        self.has_background = True

    def resizeEvent(self, event):
        if self.has_background:
            palette = QPalette()
            palette.setBrush(QPalette.Background,
                             QBrush(self.image.scaled(event.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
        super(FramelessWidget, self).resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        super(FramelessWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        self.maximum()


if __name__ == "__main__":
    from mliber_libs.qt_libs import render_ui
    with render_ui.render_ui():
        f = FramelessWidget()
        f.set_background_color(r"E:\mliber\mliber_icons\login.png")
        f.show()
