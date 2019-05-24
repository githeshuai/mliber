# -*- coding: utf-8 -*-
from Qt.QtWidgets import QFrame, QLabel, QPushButton, QHBoxLayout, QApplication, QSizePolicy
from Qt.QtCore import QSize, QTimer
import mliber_resource


class StatusBar(QFrame):
    DISPLAY_TIME = 2000

    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)
        self.setObjectName('statusWidget')
        self.setFrameShape(QFrame.NoFrame)
        self._label = QLabel(self)
        policy = (QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._label.setSizePolicy(*policy)
        self._timer = QTimer(self)
        self._button = QPushButton(self)
        self._button.setStyleSheet("QPushButton{border: 0px; padding: 0px;}")
        self._button.setMaximumSize(QSize(17, 17))
        self._button.setIconSize(QSize(17, 17))
        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 0, 0, 0)
        layout.addWidget(self._button)
        layout.addWidget(self._label)
        self.setLayout(layout)
        self.setFixedHeight(19)
        self.setMinimumWidth(5)
        self._timer.timeout.connect(self.clear)

    def error(self, text, msec=DISPLAY_TIME):
        icon = mliber_resource.icon('error.png')
        self._button.setIcon(icon)
        self._button.show()
        self._label.setStyleSheet('color: rgb(222, 0, 0);background-color: rgb(0, 0, 0, 0);')
        self.set_text(text, msec)

    def warning(self, text, msec=DISPLAY_TIME):
        icon = mliber_resource.icon("warning1.png")
        self._button.setIcon(icon)
        self._button.show()
        self._label.setStyleSheet('color: rgb(222, 180, 0);background-color: rgb(0, 0, 0, 0);')
        self.set_text(text, msec)

    def info(self, text, msec=DISPLAY_TIME):
        icon = mliber_resource.icon("info.png")
        self._button.setIcon(icon)
        self._button.show()
        self._label.setStyleSheet('background-color: rgb(0, 0, 0, 0);')
        self.set_text(text, msec)

    def set_text(self, text, msec=DISPLAY_TIME):
        if not text:
            self.clear()
        else:
            self._label.setText(text)
            self._timer.stop()
            self._timer.start(msec)
        self.update()
        self.show()

    def clear(self):
        self._timer.stop()
        self._button.hide()
        self._label.setText('')
        self._label.setStyleSheet('')
        icon = mliber_resource.icon("blank.png")
        self._button.setIcon(icon)
        self.hide()


if __name__ == "__main__":
    app = QApplication([])
    sw = StatusBar()
    sw.error("sdfasdgh")
    sw.show()
    app.exec_()
