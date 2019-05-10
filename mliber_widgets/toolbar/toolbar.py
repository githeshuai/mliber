# -*- coding:utf-8 -*-
from Qt.QtWidgets import QMenu, QAction
from Qt.QtCore import Signal
from mliber_widgets.toolbar.toolbar_ui import ToolbarUI
from mliber_widgets.login_widget import LoginWidget
import mliber_global


class Toolbar(ToolbarUI):
    user_manage_action_triggered = Signal()
    library_manage_action_triggered = Signal()

    def __init__(self, parent=None):
        super(Toolbar, self).__init__(parent)
        self._set_signals()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.settings_button.clicked.connect(self.show_settings_menu)

    def create_settings_menu(self):
        """
        创建setting菜单
        :return:
        """
        menu = QMenu(self)
        app = mliber_global.app()
        user = app.value("mliber_user")
        if user:
            if user.user_permission:
                user_manage_action = QAction("User Manager", self, triggered=self.show_user_manage)
                menu.addAction(user_manage_action)
            library_manage_action = QAction("Library Manager", self, triggered=self.show_library_manage)
            menu.addAction(library_manage_action)
        return menu

    def show_settings_menu(self):
        """
        显示settings菜单
        :return:
        """
        menu = self.create_settings_menu()
        point = self.settings_button.rect().bottomLeft()
        point = self.settings_button.mapToGlobal(point)
        menu.exec_(point)

    def show_user_manage(self):
        """
        显示user manage窗口
        :return:
        """
        self.user_manage_action_triggered.emit()

    def show_library_manage(self):
        """
        显示library manage窗口
        :return:
        """
        self.library_manage_action_triggered.emit()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = Toolbar()
        tw.show()
