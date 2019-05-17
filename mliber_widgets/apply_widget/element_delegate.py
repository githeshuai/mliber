# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QHBoxLayout, QToolButton, QVBoxLayout, QStyledItemDelegate
from Qt.QtCore import Qt, QSize
from mliber_qt_components.icon_line_edit import IconLineEdit
import mliber_resource


class CellElementWidget(QWidget):
    info_height = 24
    font_size = 10

    def __init__(self, parent=None):
        super(CellElementWidget, self).__init__(parent)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_button = QToolButton(self)
        # info layout
        info_layout = QVBoxLayout()
        self.software_le = IconLineEdit(mliber_resource.icon_path("software.png"), self.info_height, self.font_size, self)
        self.plugin_le = IconLineEdit(mliber_resource.icon_path("plugin.png"), self.info_height, self.font_size, self)
        self.path_le = IconLineEdit(mliber_resource.icon_path("folder.png"), self.info_height, self.font_size, self)
        info_layout.addWidget(self.software_le)
        info_layout.addWidget(self.plugin_le)
        info_layout.addWidget(self.path_le)
        # add to main layout
        main_layout.addWidget(self.icon_button)
        main_layout.addLayout(info_layout)

    def set_icon(self):
        """
        set icon
        :return:
        """
        # self.icon_button.setIcon()

    def set_software(self, software):
        """
        :param software: <str>
        :return:
        """
        self.software_le.setText(software)

    def set_plugin(self, plugin):
        """
        :param plugin: <str>
        :return:
        """
        self.plugin_le.setText(plugin)

    def set_path(self, path):
        """
        :param path: <str>
        :return:
        """
        self.path_le.setText(path)


class ElementDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ElementDelegate, self).__init__(parent)
        self._model = None

    def set_model(self, model):
        self._model = model

    def createEditor(self, parent, option, index):
        editor = CellElementWidget(parent)
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        item = self._get_item(index)

        editor.blockSignals(False)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        return QSize(200, 100)

    def _get_item(self, index):
        """
        get source index
        :param index:
        :return:
        """
        item = self._model.data(index, Qt.UserRole)
        return item


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        cew = CellElementWidget()
        cew.show()
