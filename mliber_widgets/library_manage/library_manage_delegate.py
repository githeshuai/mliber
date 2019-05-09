# -*- coding:utf-8 -*-
from Qt.QtWidgets import QLabel, QVBoxLayout, QToolButton, QHBoxLayout, QWidget, QStyledItemDelegate
from Qt.QtCore import Qt, QSize
import mliber_resource
from mliber_qt_components.icon_widget import IconWidget

FONT_HEIGHT = 18
PADDING = 3


class TypeWidget(QToolButton):
    def __init__(self, parent=None):
        super(TypeWidget, self).__init__(parent)
        self.setMaximumHeight(FONT_HEIGHT)
        self.setIconSize(QSize(FONT_HEIGHT * 0.8, FONT_HEIGHT * 0.8))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setIcon(mliber_resource.icon("library_type.png"))
        button_style = "QToolButton{background:transparent; border: 0px; border-radius: 0px;padding: 0px;}" \
                       "QToolButton::hover{background: transparent;}" \
                       "QToolButton:focus{outline:none;border: 0px; border-radius: 0px;}"
        self.setStyleSheet(button_style)

    def mousePressEvent(self, event):
        """
        取消事件
        :param event:
        :return:
        """
        event.ignore()


class CellLibrary(QWidget):
    def __init__(self, parent=None):
        super(CellLibrary, self).__init__(parent)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(PADDING, 0, PADDING, 0)
        type_layout = QHBoxLayout()
        type_layout.setContentsMargins(0, 0, 0, 0)
        # type button
        self.type_button = TypeWidget(self)
        type_layout.addStretch()
        type_layout.addWidget(self.type_button)
        # icon label
        self.icon_widget = IconWidget(self)
        # name label
        self.name_label = QLabel(self)
        self.name_label.setStyleSheet("background: transparent;")
        self.name_label.setMaximumHeight(FONT_HEIGHT)
        self.name_label.setAlignment(Qt.AlignCenter)
        # add to main layout
        main_layout.addLayout(type_layout)
        main_layout.addWidget(self.icon_widget)
        main_layout.addWidget(self.name_label)
        main_layout.setSpacing(2)

    def set_icon(self, icon):
        """
        设置显示图片
        :return:
        """
        self.icon_widget.set_icon(icon)

    def set_icon_size(self, size):
        """
        set icon label size
        :param size:
        :return:
        """
        self.icon_widget.set_icon_size(size)

    def set_name(self, name):
        """
        设置名字
        :return:
        """
        self.name_label.setText(name)

    def set_type(self, typ):
        """
        :param typ: <str>
        :return:
        """
        self.type_button.setText(typ)


class LibraryManageDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(LibraryManageDelegate, self).__init__(parent)
        self.__parent = parent

    def createEditor(self, parent, option, index):
        editor = CellLibrary(parent)
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        item = self.get_item(index)
        editor.set_icon_size(item.icon_size)
        editor.set_icon(self.__parent.image_server.get_image(item.icon_path))
        editor.set_name(item.library.name)
        editor.set_type(item.library.type)
        editor.blockSignals(False)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        item = self.get_item(index)
        size = QSize(item.icon_size.width()+2*PADDING, item.icon_size.height()+FONT_HEIGHT*2)
        return size

    @staticmethod
    def get_item(index):
        """
        get source index
        :param index:
        :return:
        """
        source_model = index.model().sourceModel()
        source_index = index.model().mapToSource(index)
        item = source_model.data(source_index, Qt.UserRole)
        return item
