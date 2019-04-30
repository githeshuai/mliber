# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from mliber_widgets.toolbar.toolbar_ui import ToolbarUI
from mliber_widgets.login_widget import LoginWidget
import mliber_global
from mliber_widgets.user_manage import UserManage


class Toolbar(ToolbarUI):
    def __init__(self, parent=None):
        super(Toolbar, self).__init__(parent)
        self._set_signals()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.login_button.clicked.connect(self.show_login)
        self.settings_button.clicked.connect(self.show_settings_menu)

    def show_login(self):
        """
        显示login ui
        :return:
        """
        login_widget = LoginWidget(self)
        login_widget.move_to_center()
        login_widget.exec_()

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
        user_manage_ui = UserManage()
        user_manage_ui.exec_()

    def show_library_manage(self):
        """
        显示library manage窗口
        :return:
        """
        return


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = Toolbar()
        tw.show()
