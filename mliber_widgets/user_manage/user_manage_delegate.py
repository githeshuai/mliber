# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class UserManageDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(UserManageDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() in xrange(6, 12):
            editor = QComboBox(parent)
            editor.setFocusPolicy(Qt.NoFocus)
            if index.column() == 11:
                editor.addItems(["Active", "Disable"])
            else:
                editor.addItems(["True", "False"])
            editor.currentIndexChanged.connect(self.onCurrentIndexChanged)
            return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        if isinstance(editor, QComboBox):
            value = index.model().data(index, Qt.UserRole)
            editor.setCurrentIndex(editor.findText(value))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.UserRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        return QSize(160, 20)

    def onCurrentIndexChanged(self, index):
        self.commitData.emit(self.sender())
