# -*- coding:utf-8 -*-
from Qt.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QDialog
from user_manage_table_view import UserTableView
from mliber_api.database_api import Database
import mliber_global
import mliber_resource


class UserManage(QDialog):
    def __init__(self, parent=None):
        super(UserManage, self).__init__(parent)
        self.resize(1200, 500)
        self.setWindowTitle("User Manager")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.user_table_view = UserTableView(self)
        main_layout.addWidget(self.user_table_view)
        # button layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        self.add_btn = QPushButton("Add")
        self.refresh_button = QPushButton("Refresh")
        self.apply_btn = QPushButton("Apply")
        self.close_button = QPushButton("Close")
        button_layout.addWidget(self.add_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.close_button)
        main_layout.addLayout(button_layout)
        # set style sheet
        self._set_style()
        self._set_signals()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.add_btn.clicked.connect(self._add_user)
        self.refresh_button.clicked.connect(self.refresh_table)
        self.apply_btn.clicked.connect(self._apply)
        self.close_button.clicked.connect(self.close)

    def _set_style(self):
        """
        set style sheet
        :return:
        """
        self.setStyleSheet(mliber_resource.style())

    def _add_user(self):
        """
        添加用户
        :return:
        """
        model = self.user_table_view.model()
        row_count = model.rowCount()
        model.insertRows(row_count+1, 1)
        self.user_table_view.show_delegate()

    @staticmethod
    def __str_to_bool(value):
        """
        将str转换为bool
        :return:
        """
        if value == "True":
            return True
        return False

    def _apply(self):
        """
        完成创建或者更新
        :return:
        """
        app = mliber_global.app()
        db = Database(app.value("mliber_database"))
        app_user = app.value("mliber_user")
        model_data = self.user_table_view.model().model_data
        if not model_data:
            return
        for each_user in model_data:
            user_id, name, chinese_name, password, created_at, created_by, user_permission, library_permission, \
                category_permission, asset_permission, tag_permission, status, description = each_user
            user_data_dict = {"name": name,
                              "chinese_name": chinese_name,
                              "password": password,
                              "user_permission": self.__str_to_bool(user_permission),
                              "library_permission": self.__str_to_bool(library_permission),
                              "category_permission": self.__str_to_bool(category_permission),
                              "asset_permission": self.__str_to_bool(asset_permission),
                              "tag_permission": self.__str_to_bool(tag_permission),
                              "status": status,
                              "description": description}
            if user_id:
                user_id = int(user_id)
                db.update("User", user_id, user_data_dict)
            else:
                user_data_dict.update({"created_by": app_user.id})
                db.create("User", user_data_dict)
        self.refresh_table()

    def refresh_table(self):
        """
        刷新table view
        :return:
        """
        self.user_table_view.show_data()
