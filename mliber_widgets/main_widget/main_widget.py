# -*- coding:utf-8 -*-
from main_widget_ui import MainWidgetUI
from mliber_widgets.user_manage import UserManage
from mliber_widgets.library_manage import LibraryManage
import mliber_utils
import mliber_global
import mliber_resource
from mliber_api.database_api import Database
from mliber_qt_components.messagebox import MessageBox


class MainWidget(MainWidgetUI):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        # set style
        self.set_style()
        # set signals
        self.set_signals()

    def set_style(self):
        """
        set style
        :return:
        """
        return self.setStyleSheet(mliber_resource.style())

    @property
    def db(self):
        database = mliber_global.app().value("mliber_database")
        return Database(database)

    @property
    def library(self):
        return mliber_global.app().value("mliber_library")

    def set_signals(self):
        """
        信号连接
        :return:
        """
        self.tool_bar.user_manage_action_triggered.connect(self.show_user_manager)
        self.tool_bar.library_manage_action_triggered.connect(self.show_library_manager)
        self.category_widget.category_tree.itemSelectionChanged.connect(self._on_category_selection_changed)
        self.tag_widget.tag_list_view.selection_changed.connect(self._on_tag_selection_changed)

    def show_user_manager(self):
        """
        显示user manager
        :return:
        """
        user_manage_ui = UserManage(self)
        user_manage_ui.exec_()

    def show_library_manager(self):
        """
        显示library manager
        :return:
        """
        library_manage_ui = LibraryManage(self)
        library_manage_ui.refresh_ui()
        library_manage_ui.library_double_clicked.connect(self.refresh_library)
        library_manage_ui.exec_()

    def assets_of_library(self, library_id):
        """
        获取该library下所有的资产
        :param library_id:
        :return:
        """
        filters = [["library_id", "=", library_id], ["status", "=", "Active"]]
        assets = self.db.find("Asset", filters)
        return assets

    def tags_of_assets(self, assets):
        """
        获取该library下所有资产的tag
        :param assets: <list> Asset instance list
        :return:
        """
        tags = list()
        asset_tags = list()
        for asset in assets:
            asset_tags.extend(asset.tags)
        if asset_tags:
            tag_names = [tag.name for tag in asset_tags]
            tag_names = list(set(tag_names))
            tags = self.db.find("Tag", [["name", "in", tag_names], ["status", "=", "Active"]])
        return tags

    def _on_category_selection_changed(self):
        """
        当category选择改变的时候
        :return:
        """
        print "category changed"

    def _on_tag_selection_changed(self, tags):
        """
        当tag选择改变的时候
        :return:
        """
        print tags

    def refresh_library(self):
        """
        刷新library, 切换library的时候，
        获取所有的category和所有的assets，列出当前类别下所有的tag
        :return:
        """
        # 获取所有的assets, 显示在asset list view中
        if not self.library:
            self.category_widget.clear()
            self.tag_widget.clear()
            return
        # 列出所有的category
        self.category_widget.refresh_ui()
        # 求出所有资产
        assets = self.assets_of_library(self.library.id)
        self.asset_widget.set_assets(assets)
        # 列出所有的tag
        tags = self.tags_of_assets(assets)
        self.tag_widget.tag_list_view.show_data(tags)
        tag_names = [tag.name for tag in tags]
        self.tag_widget.set_completer(tag_names)

    def auto_login(self):
        """
        自动登录
        :return:
        """
        app = mliber_global.app()
        need_remember = mliber_utils.read_history("need_remember")
        auto_login = mliber_utils.read_history("auto_login")
        if need_remember and auto_login:
            try:
                database = mliber_utils.read_history("database")
                user_name = mliber_utils.read_history("user")
                password = mliber_utils.read_history("password")
                db = Database(database)
                db.create_admin()
                app.set_value(mliber_database=database)
                user = db.find_one("User", [["name", "=", user_name], ["status", "=", "Active"]])
                if user and user.password == password:
                    app.set_value(mliber_user=user)
            except RuntimeError as e:
                MessageBox.critical(self, "Login Failed", str(e))
                return False
        return True

    def set_global_library_from_history(self):
        """
        根据历史记录获取library，并设置全局
        :return:
        """
        app = mliber_global.app()
        library_id = mliber_utils.read_history("library_id")
        if library_id:
            library = self.db.find_one("Library",
                                       [["id", "=", library_id],
                                        ["status", "=", "Active"]])
            if library:
                app.set_value(mliber_library=library)
            else:
                app.set_value(mliber_library=None)
            self.refresh_library()

    def showEvent(self, event):
        """
        在显示之前，获取历史记录，自动登录
        :return:
        """
        # 自动登录
        if self.auto_login():
            self.set_global_library_from_history()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        mw = MainWidget()
        mw.show()
