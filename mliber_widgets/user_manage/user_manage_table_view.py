# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from mliber_global.app_global import get_app_global
from user_manage_model import UserManageModel
from user_manage_delegate import UserManageDelegate


class UserTableView(QTableView):
    def __init__(self, parent=None):
        super(UserTableView, self).__init__(parent)
        self.show_data()
        self.horizontalHeader().setStretchLastSection(True)
        self.setFocusPolicy(Qt.NoFocus)

    @staticmethod
    def _get_model_data():
        """
        从数据库中获取user
        :return:
        """
        model_data = list()
        app_global = get_app_global()
        db = app_global.value("mliber_database")
        users = db.find("User", [])
        for user in users:
            temp = [user.id, user.name, user.chinese_name, user.password, user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    user.created_by, str(user.user_permission), str(user.library_permission),
                    str(user.category_permission), str(user.asset_permission), str(user.tag_permission),
                    user.status, user.description]
            model_data.append(temp)
        return model_data

    def _set_model(self):
        """
        set model
        :return:
        """
        model_data = self._get_model_data()
        header_list = ["id", "name", "chinese name", "password", "created at", "created by", "user permission",
                       "library permission", "category permission", "asset permission",
                       "tag permission", "status", "description"]
        model = UserManageModel(model_data, self)
        model.set_header(header_list)
        self.setModel(model)

    def _set_delegate(self):
        """
        设置代理
        :return:
        """
        delegate = UserManageDelegate(self)
        for column in xrange(6, 12):
            self.setItemDelegateForColumn(column, delegate)
        self.show_delegate()

    def show_delegate(self):
        """
        显示代理
        :return:
        """
        for row in xrange(self.model().rowCount()):
            for column in xrange(6, 12):
                self.openPersistentEditor(self.model().index(row, column))

    def show_data(self):
        """
        刷新ui
        :return:
        """
        self._set_model()
        self._set_delegate()
