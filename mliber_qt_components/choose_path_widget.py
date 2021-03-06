# -*- coding: utf-8 -*-
from Qt.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog


class ChoosePathWidget(QWidget):
    def __init__(self, parent=None):
        super(ChoosePathWidget, self).__init__(parent)

        self._filter = "*.png"

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self)
        self.label.setMinimumWidth(30)
        self.label.setScaledContents(True)
        self.le = QLineEdit(self)
        self.btn = QPushButton("Browse", self)
        self.btn.setMaximumHeight(25)
        layout.addWidget(self.label)
        layout.addWidget(self.le)
        layout.addWidget(self.btn)
        # set signals
        self._set_signals()

    def set_filter(self, filter_str):
        """
        set choose path filter
        :param filter_str:
        :return:
        """
        self._filter = filter_str

    def set_label_text(self, text):
        """
        set label text
        :param text: <str>
        :return:
        """
        self.label.setText(text)

    def set_place_holder_text(self, text):
        """
        set line edit place holder text
        :param text: <str>
        :return:
        """
        self.le.setPlaceholderText(text)

    def set_btn_text(self, text):
        """
        set button text
        :param text:
        :return:
        """
        self.btn.setText(text)

    @property
    def path(self):
        """
        :return:
        """
        return self.le.text()

    def set_path(self, path):
        """
        set path
        :return:
        """
        self.le.setText(path)

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.btn.clicked.connect(self.choose_path)

    def choose_path(self):
        """
        选择路径
        :return:
        """
        path, ext = QFileDialog.getOpenFileName(self, "image", filter="Files (%s)" % self._filter)
        if path:
            self.le.setText(path)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        c = ChoosePathWidget()
        c.show()
