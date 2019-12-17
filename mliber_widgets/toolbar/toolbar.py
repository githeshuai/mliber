# -*- coding:utf-8 -*-
from Qt.QtWidgets import QMenu, QAction
from Qt.QtCore import Signal
from mliber_widgets.toolbar.toolbar_ui import ToolbarUI
import mliber_global
import mliber_resource
from mliber_qt_components.messagebox import MessageBox


class Toolbar(ToolbarUI):
    user_manage_action_triggered = Signal()
    library_manage_action_triggered = Signal()
    change_password_action_triggered = Signal()
    my_favorites_action_triggered = Signal()
    clear_trash_action_triggered = Signal()
    modify_settings_signal = Signal()

    def __init__(self, parent=None):
        super(Toolbar, self).__init__(parent)
        self._create_settings_menu()
        self._create_user_menu()

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
        self.manager_button.set_menu()
        self.manager_button.add_menu_action("User Manager", self._show_user_manage)
        self.manager_button.add_menu_action("Library Manager", self._show_library_manage)

    def _show_user_manage(self):
        """
        显示user manage窗口
        :return:
        """
        user = mliber_global.user()
        if not user:
            MessageBox.warning(self, "Warning", "Login First")
            return
        if user.user_permission:
            self.user_manage_action_triggered.emit()
        else:
            MessageBox.warning(self, "Warning", "Permission denied")

    def _show_library_manage(self, *args):
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
        self.user_button.set_menu()
        self.user_button.add_menu_action("Change Password", self._change_password)
        self.user_button.add_menu_action("My Favorites", self._show_my_favorites)
        self.user_button.add_menu_action("Settings", self._show_settings)
        self.user_button.add_menu_separator()
        self.user_button.add_menu_action("Clear Trash", self._clear_trash, icon_name="delete.png")

    def _change_password(self):
        """
        :return:
        """
        user = mliber_global.user()
        if not user:
            MessageBox.warning(self, "Warning", "Login First")
            return
        self.change_password_action_triggered.emit()

    def _show_my_favorites(self):
        """
        :return:
        """
        if not mliber_global.user():
            MessageBox.warning(self, "Warning", "Login First.")
            return
        self.my_favorites_action_triggered.emit()

    def _show_settings(self):
        """
        show setting dialog
        :return:
        """
        if not mliber_global.user():
            MessageBox.warning(self, "Warning", "Login First.")
            return
        from mliber_widgets.settings_widget import SettingsDialog
        sd = SettingsDialog(self)
        sd.setting_finished_signal.connect(self.modify_settings_signal)
        sd.exec_()

    def _clear_trash(self):
        """
        :return:
        """
        user = mliber_global.user()
        if user and user.database_permission:
            self.clear_trash_action_triggered.emit()
        else:
            MessageBox.warning(self, "Warning", "Permission denied")


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = Toolbar()
        tw.show()
