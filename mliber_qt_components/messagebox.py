# -*- coding: utf-8 -*-
from Qt.QtWidgets import QDialog, QDialogButtonBox, QFrame, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from Qt.QtCore import Qt
import mliber_resource


class MessageBox(QDialog):

    @staticmethod
    def information(parent, title, message, options=QDialogButtonBox.Ok, size=None):
        mb = MessageBox(parent)
        if size:
            mb.setFixedSize(size)
        mb.setText(message)
        mb.setOptions(options)
        mb.header().setStyleSheet('background-color: rgb(7,171,172);')
        p = mliber_resource.pixmap('information.png')
        mb.setPixmap(p)
        mb.setWindowTitle(title)
        mb.setTitleText(title)
        a = mb.exec_()
        return mb._standardButtonClicked

    @staticmethod
    def warning(parent, title, message, options=QDialogButtonBox.Ok):
        mb = MessageBox(parent)
        mb.setText(message)
        mb.setOptions(options)
        mb.header().setStyleSheet('background-color: rgb(196,196,51);')
        p = mliber_resource.pixmap('warning.png')
        mb.setPixmap(p)
        mb.setWindowTitle(title)
        mb.setTitleText(title)
        a = mb.exec_()
        return mb._standardButtonClicked

    @staticmethod
    def question(parent, title, message, options=QDialogButtonBox.Yes | QDialogButtonBox.No):
        mb = MessageBox(parent)
        mb.setText(message)
        mb.setOptions(options)
        mb.header().setStyleSheet('background-color: rgb(50,150,200);')
        p = mliber_resource.pixmap('question.png')
        mb.setPixmap(p)
        mb.setWindowTitle(title)
        mb.setTitleText(title)
        a = mb.exec_()
        return mb._standardButtonClicked

    @staticmethod
    def critical(parent, title, message, options=QDialogButtonBox.Ok):
        mb = MessageBox(parent)
        mb.setText(message)
        mb.setOptions(options)
        mb.header().setStyleSheet('background-color: rgb(200,50,50);')
        p = mliber_resource.pixmap('critical.png')
        mb.setPixmap(p)
        mb.setWindowTitle(title)
        mb.setTitleText(title)
        a = mb.exec_()
        return mb._standardButtonClicked

    def __init__(self, parent=None):
        super(MessageBox, self).__init__(parent)
        self.setMinimumWidth(300)
        self._standardButtonClicked = None
        self._header = QFrame(self)
        self._header.setStyleSheet('background-color: rgb(50,150,200,0);')
        self._header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._header.setFixedHeight(46)
        self._icon = QLabel()
        self._icon.setAlignment(Qt.AlignTop)
        self._icon.setScaledContents(True)
        self._icon.setFixedWidth(28)
        self._icon.setFixedHeight(28)
        self._icon.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._title = QLabel(self._header)
        self._title.setStyleSheet('font: 14pt bold; color:rgb(255,255,255);')
        self._title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        hlayout = QHBoxLayout(self._header)
        hlayout.setSpacing(10)
        hlayout.addWidget(self._icon)
        hlayout.addWidget(self._title)

        self._message = QLabel()
        self._message.setMinimumHeight(50)
        self._message.setWordWrap(True)
        self._message.setAlignment(Qt.AlignLeft)
        self._message.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self._message.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._buttonBox = QDialogButtonBox(None, Qt.Horizontal, self)
        self._buttonBox.clicked.connect(self._clicked)
        self._buttonBox.accepted.connect(self._accept)
        self._buttonBox.rejected.connect(self._reject)
        vlayout1 = QVBoxLayout(self)
        vlayout1.setContentsMargins(0, 0, 0, 0)
        vlayout1.addWidget(self._header)
        vlayout2 = QVBoxLayout()
        vlayout2.setSpacing(25)
        vlayout2.setContentsMargins(15, 5, 15, 5)
        vlayout2.addWidget(self._message)
        vlayout2.addWidget(self._buttonBox)
        vlayout1.addLayout(vlayout2)

    def _accept(self):
        self.accept()
        self.deleteLater()

    def _reject(self):
        self.reject()
        self.deleteLater()
    
    def header(self):
        return self._header

    def setTitleText(self, text):
        self._title.setText(text)

    def setText(self, message):
        self._message.setText(message)

    def setOptions(self, options):
        self._buttonBox.setStandardButtons(options)

    def setPixmap(self, pixmap):
        self._icon.setPixmap(pixmap)

    def _clicked(self, button):
        self._standardButtonClicked = self._buttonBox.standardButton(button)
