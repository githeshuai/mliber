# -*- coding:utf-8 -*-
from Qt.QtWidgets import QMenu, QAction
from Qt.QtCore import Signal
from mliber_widgets.toolbar.toolbar_ui import ToolbarUI
import mliber_global


class Toolbar(ToolbarUI):
    user_manage_action_triggered = Signal()
    library_manage_action_triggered = Signal()
    change_password_action_triggered = Signal()
    my_favorites_action_triggered = Signal()

    def __init__(self, parent=None):
        super(Toolbar, self).__init__(parent)
        self._set_signals()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.settings_button.clicked.connect(self._show_settings_menu)
        self.user_button.clicked.connect(self._show_user_menu)

    def set_user(self, user_name):
        """
        设置当前用户
        :param user_name: <str>
        :return:
        """
        self.user_button.setText(user_name)

    def _create_settings_menu(self):
        """
        创建setting菜单
        :return:
        """
        menu = QMenu(self)
        user = mliber_global.user()
        if user:
            if user.user_permission:
                user_manage_action = QAction("User Manager", self, triggered=self._show_user_manage)
                menu.addAction(user_manage_action)
            library_manage_action = QAction("Library Manager", self, triggered=self._show_library_manage)
            menu.addAction(library_manage_action)
        return menu

    def _show_settings_menu(self):
        """
        显示settings菜单
        :return:
        """
        menu = self._create_settings_menu()
        point = self.settings_button.rect().bottomLeft()
        point = self.settings_button.mapToGlobal(point)
        menu.exec_(point)

    def _show_user_manage(self):
        """
        显示user manage窗口
        :return:
        """
        self.user_manage_action_triggered.emit()

    def _show_library_manage(self):
        """
        显示library manage窗口
        :return:
        """
        self.library_manage_action_triggered.emit()
        
    def _create_user_menu(self):
        """
        创建用户menu
        :return:
        """
        menu = QMenu(self)
        change_password_action = QAction("Change Password", self, triggered=self._change_password)
        my_favorite_action = QAction("My Favorites", self, triggered=self._show_my_favorites)
        menu.addAction(change_password_action)
        menu.addAction(my_favorite_action)
        return menu

    def _show_user_menu(self):
        """
        显示用户menu
        :return:
        """
        if mliber_global.user():
            menu = self._create_user_menu()
            point = self.user_button.rect().bottomLeft()
            point = self.user_button.mapToGlobal(point)
            menu.exec_(point)

    def _change_password(self):
        """
        :return:
        """
        self.change_password_action_triggered.emit()

    def _show_my_favorites(self):
        """
        :return:
        """
        self.my_favorites_action_triggered.emit()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = Toolbar()
        tw.show()
