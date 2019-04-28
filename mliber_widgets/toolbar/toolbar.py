# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from mliber_widgets.toolbar.toolbar_ui import ToolbarUI
from mliber_widgets.login_widget import LoginWidget


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

    def show_login(self):
        """
        显示login ui
        :return:
        """
        login_widget = LoginWidget(self)
        login_widget.move_to_center()
        login_widget.exec_()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = Toolbar()
        tw.show()
