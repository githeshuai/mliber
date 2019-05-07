# -*- coding:utf-8 -*-
from Qt.QtWidgets import QToolButton, QStyledItemDelegate
from Qt.QtCore import Qt, QSize
import mliber_resource


TAG_HEIGHT = 20


class CellTag(QToolButton):
    def __init__(self, parent=None):
        super(CellTag, self).__init__(parent)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setFixedHeight(TAG_HEIGHT)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background: transparent; border: 0px solid; padding: 0px; "
                           "border-radius: 10px; color: #fff;")
        self.setFocusPolicy(Qt.NoFocus)
        self.set_icon()

    def set_icon(self):
        """
        set tag icon
        :return:
        """
        self.setIconSize(QSize(TAG_HEIGHT*0.8, TAG_HEIGHT*0.8))
        self.setIcon(mliber_resource.icon("tag.png"))

    def set_text(self, text):
        """
        set text
        :return:
        """
        self.setText(text)

    def mousePressEvent(self, event):
        """
        取消事件
        :param event:
        :return:
        """
        event.ignore()


class TagDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TagDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        self.editor = CellTag(parent)
        return self.editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        tag = self.get_tag_item(index)
        editor.set_text(tag.text())
        editor.blockSignals(False)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        tag = self.get_tag_item(index)
        return QSize(tag.width(), TAG_HEIGHT)

    @staticmethod
    def get_tag_item(index):
        """
        get source index
        :param index:
        :return:
        """
        source_model = index.model().sourceModel()
        source_index = index.model().mapToSource(index)
        tag = source_model.data(source_index, Qt.UserRole)
        return tag
