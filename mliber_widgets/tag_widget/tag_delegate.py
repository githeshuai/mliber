# -*- coding:utf-8 -*-
from Qt.QtWidgets import QToolButton, QStyledItemDelegate
from Qt.QtCore import Qt, QSize
import mliber_resource
from mliber_qt_components.icon import Icon


TAG_HEIGHT = 22


class CellTag(QToolButton):
    def __init__(self, parent=None):
        super(CellTag, self).__init__(parent)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setFixedHeight(TAG_HEIGHT)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background: transparent; border: 0px solid; padding: 0px; font-size: 12px;"
                           "border-radius: 10px; color: #000; color: rgb(255, 255, 255, 180);")
        self.setFocusPolicy(Qt.NoFocus)

    def set_icon_color(self, color):
        """
        set tag icon
        :return:
        """
        self.setIconSize(QSize(TAG_HEIGHT*0.8, TAG_HEIGHT*0.8))
        icon = Icon(mliber_resource.icon_path("tag.png"))
        icon.set_color(color)
        self.setIcon(icon)

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
        item = self.get_tag_item(index)
        editor.set_icon_color(item.color)
        editor.set_text(item.name)
        editor.blockSignals(False)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        tag = self.get_tag_item(index)
        return QSize(tag.width, TAG_HEIGHT)

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
