# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from mliber_widgets.title_widget.title_widget_ui import TitleWidgetUI
from mliber_custom.database import DATABASES
from mliber_global.app_global import get_app_global
from mliber_api.database_api import Database


class TitleWidget(TitleWidgetUI):
    def __init__(self, parent=None):
        super(TitleWidget, self).__init__(parent)
        self.database_action_group = QActionGroup(self)
        self._set_signals()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.database_button.clicked.connect(self.init_database)
        self.database_action_group.triggered.connect(self.switch_database)

    def _create_database_menu(self):
        """
        创建database menu
        :return:
        """
        database_menu = QMenu(self)
        databases = DATABASES.keys()
        for database in databases:
            action = QAction(database, self)
            action.setCheckable(True)
            database_menu.addAction(action)
            self.database_action_group.addAction(action)
        return database_menu

    def init_database(self):
        """
        显示database menu
        :return:
        """
        menu = self._create_database_menu()
        point = self.database_button.rect().bottomLeft()
        point = self.database_button.mapToGlobal(point)
        menu.exec_(point)

    def switch_database(self, action):
        """
        切换数据库
        :return:
        """
        database = action.text()
        app_global = get_app_global()
        app_global.set_value(mliber_database=database)
        database_api_instance = Database(database)
        app_global.set_value(mliber_database=database_api_instance)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = TitleWidget()
        tw.show()
