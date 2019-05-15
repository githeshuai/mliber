# -*- coding: utf-8 -*-
from Qt.QtWidgets import QDialog, QVBoxLayout, QFrame, QSizePolicy, QHBoxLayout, QLabel, \
    QScrollArea, QWidget, QTextEdit, QPushButton
from Qt.QtGui import *
from Qt.QtCore import Signal, Qt
import mliber_resource


class InputTextEdit(QDialog):
    editTextFinished = Signal(basestring)

    def __init__(self, parent=None):
        super(InputTextEdit, self).__init__(parent)

        self.resize(350, 360)
        self.setWindowTitle("Selected")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame(self)
        header.setStyleSheet('background-color: rgb(7,171,172);')
        header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        header.setFixedHeight(46)
        title_layout = QHBoxLayout(header)
        title_layout.setSpacing(20)
        title_layout.setContentsMargins(0, 0, 0, 0)
        icon_label = QLabel(self)
        icon_label.setPixmap(mliber_resource.pixmap("information.png"))
        icon_label.setScaledContents(True)
        icon_label.setFixedWidth(28)
        icon_label.setFixedHeight(28)
        icon_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.title_label = QLabel(self)
        self.title_label.setFixedHeight(46)
        self.title_label.setStyleSheet('font: 14pt bold; color:rgb(255,255,255);')
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        title_layout.addWidget(icon_label)
        title_layout.addWidget(self.title_label)

        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFocusPolicy(Qt.NoFocus)
        widget = QWidget()
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.text_edit = QTextEdit()
        self.text_edit.setFontPointSize(10)
        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(3)
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        main_layout.addWidget(header)
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(btn_layout)
        main_layout.setSpacing(0)
        self._set_signals()

    def _set_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.ok_btn.clicked.connect(self.on_ok_btn_clicked)

    def set_data(self, value):
        """
        Args:
            value: <list>
        Returns:
        """
        self.text_edit.setText("")
        data = "\n".join(value)
        self.text_edit.setText(data)

    def set_title(self, title):
        self.title_label.setText(title)

    def on_ok_btn_clicked(self):
        self.accept()
        self.editTextFinished.emit(self.data())
        self.deleteLater()

    def on_cancel_btn_clicked(self):
        self.reject()
        self.deleteLater()

    def data(self):
        return self.text_edit.toPlainText()
