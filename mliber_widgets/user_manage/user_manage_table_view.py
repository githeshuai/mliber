# -*- coding:utf-8 -*-
from Qt.QtWidgets import QTableView
from Qt.QtCore import Qt
import mliber_global
from user_manage_model import UserManageModel
from user_manage_delegate import UserManageDelegate
from mliber_api.database_api import Database


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
        app = mliber_global.app()
        db = Database(app.value("mliber_database"))
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
        header_list = ["id", u"名字", u"中文名", u"密码", u"创建时间", u"创建者", u"用户权限",
                       u"库权限", u"类别权限", u"资产权限", u"标签权限", u"状态", u"描述"]
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
        self.show_delegate()
