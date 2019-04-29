# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class UserManageDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(UserManageDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() in [1, 2, 3, 12]:
            editor = QLineEdit(parent)
            return editor
        if index.column() in [6, 7, 8, 9, 10]:
            editor = QComboBox(parent)
            editor.addItems(["True", "False"])
            editor.currentIndexChanged.connect(self.onCurrentIndexChanged)
            return editor
        if index.column() == 11:
            editor = QComboBox(parent)
            editor.addItems(["Active", "Disable"])
            editor.currentIndexChanged.connect(self.onCurrentIndexChanged)
            return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        if isinstance(editor, QLineEdit):
            value = index.model().data(index, Qt.DisplayRole)
            editor.setText(value)
        if isinstance(editor, QComboBox):
            value = index.model().data(index, Qt.UserRole)
            editor.setCurrentIndex(editor.findText(str(value)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QLineEdit):
            value = editor.text()
            model.setData(index, value, Qt.DisplayRole)
        if isinstance(editor, QComboBox):
            value = editor.currentText()
            model.setData(index, value, Qt.UserRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        return QSize(160, 20)

    def onCurrentIndexChanged(self, index):
        self.commitData.emit(self.sender())