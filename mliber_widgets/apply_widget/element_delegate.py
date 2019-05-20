# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QHBoxLayout, QToolButton, QVBoxLayout, QStyledItemDelegate, QMenu, QAction
from Qt.QtCore import Qt, QSize
from mliber_qt_components.toolbutton import ToolButton
from mliber_qt_components.icon_line_edit import IconLineEdit
import mliber_resource
import mliber_utils
from mliber_parse.element_type_parser import ElementType


class CellElementWidget(QWidget):
    info_height = 24
    font_size = 11

    def __init__(self, parent=None):
        super(CellElementWidget, self).__init__(parent)
        self._element_type = None
        self._path = None
        self.setAutoFillBackground(True)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_button = ToolButton(self)
        self.icon_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.icon_button.setStyleSheet("background: transparent; padding: 0px;")
        # info layout
        info_layout = QVBoxLayout()
        style_sheet = "QLineEdit{border: 0px solid; background: transparent; padding-left: 25; color: #8A8A8A;}"
        self.software_le = IconLineEdit(mliber_resource.icon_path("software.png"), self.info_height, self.font_size, self)
        self.software_le.setReadOnly(True)
        self.software_le.setPlaceholderText("Software")
        self.software_le.setStyleSheet(style_sheet)
        self.plugin_le = IconLineEdit(mliber_resource.icon_path("plugin.png"), self.info_height, self.font_size, self)
        self.plugin_le.setPlaceholderText("Plugin")
        self.plugin_le.setStyleSheet(style_sheet)
        self.plugin_le.setReadOnly(True)
        self.path_le = IconLineEdit(mliber_resource.icon_path("folder.png"), self.info_height, self.font_size, self)
        self.path_le.setPlaceholderText("Path")
        self.path_le.setStyleSheet(style_sheet)
        self.path_le.setReadOnly(True)
        info_layout.addWidget(self.software_le)
        info_layout.addWidget(self.plugin_le)
        info_layout.addWidget(self.path_le)
        info_layout.setSpacing(0)
        # add to main layout
        main_layout.addWidget(self.icon_button)
        main_layout.addLayout(info_layout)
        main_layout.setSpacing(0)
        # set signals
        self.set_signals()

    def set_signals(self):
        """
        :return:
        """
        self.icon_button.clicked.connect(self._show_action_menu)

    def set_type(self, typ):
        """
        set icon
        :return:
        """
        self._element_type = typ
        icon_path = ElementType(typ).icon
        self.icon_button.setText(typ)
        self.icon_button.set_icon(icon_path)
        self.icon_button.setFixedSize(QSize(60, 60))
        self.icon_button.setIconSize(QSize(42, 42))

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
        self._path = path
        self.path_le.setText(path)

    def _create_action_menu(self):
        """
        创建action菜单
        :return:
        """
        menu = QMenu(self)
        engine = mliber_utils.engine()
        actions = ElementType(self._element_type).import_actions_of_engine(engine)
        for action in actions:
            q_action = QAction(action.name, self, triggered=self.run_hook)
            q_action.hook = action.hook
            menu.addAction(q_action)
        return menu

    def _show_action_menu(self):
        """
        显示菜单
        :return:
        """
        menu = self._create_action_menu()
        point = self.icon_button.rect().bottomLeft()
        point = self.icon_button.mapToGlobal(point)
        menu.exec_(point)

    def run_hook(self):
        """
        运行主函数
        :return:
        """
        hook_name = self.sender().hook
        hook_module = mliber_utils.load_hook(hook_name)
        hook_instance = hook_module.Hook(self._path)
        hook_instance.main()


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
        editor.set_type(item.type)
        editor.set_software(item.software)
        editor.set_plugin(item.plugin)
        editor.set_path(item.path)
        editor.blockSignals(False)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        return QSize(200, 60)

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
