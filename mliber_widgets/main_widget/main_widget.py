# -*- coding:utf-8 -*-
from main_widget_ui import MainWidgetUI
from mliber_widgets.login_widget import LoginWidget
from mliber_widgets.user_manage import UserManage
from mliber_widgets.library_manage import LibraryManage
from mliber_widgets.apply_widget import ApplyWidget
import mliber_utils
import mliber_global
import mliber_resource
from mliber_api.database_api import Database
from mliber_qt_components.messagebox import MessageBox
from mliber_widgets import create_widget


class MainWidget(MainWidgetUI):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.right_is_shown = False
        # set style
        self._set_style()
        # set signals
        self._set_signals()

    def _set_style(self):
        """
        set style
        :return:
        """
        return self.setStyleSheet(mliber_resource.style())

    @property
    def library(self):
        return mliber_global.library()

    @property
    def library_type(self):
        if self.library:
            return self.library.type

    @property
    def category(self):
        categories = mliber_global.categories()
        if categories and len(categories):
            return categories[0]

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.tool_bar.login_button.clicked.connect(self.show_login)
        self.tool_bar.user_manage_action_triggered.connect(self.show_user_manager)
        self.tool_bar.library_manage_action_triggered.connect(self.show_library_manager)
        self.category_widget.category_tree.selection_changed.connect(self._on_category_selection_changed)
        self.tag_widget.tag_list_view.selection_changed.connect(self._on_tag_selection_changed)
        self.asset_widget.asset_list_view.add_tag_signal.connect(self._add_tag)
        self.asset_widget.export_from_software.connect(self._show_create_widget)
        self.asset_widget.asset_list_view.left_pressed.connect(self._show_apply)

    def _get_children_categories(self, categories):
        """
        获取子类型，需要递归
        :param categories: <list> list of Category
        :return:
        """
        all_categories = list()

        def get(category_list):
            category_id_list = [category.id for category in category_list]
            with mliber_global.db() as db:
                children_categories = db.find("Category", [["parent_id", "in", category_id_list]])
                if children_categories:
                    all_categories.extend(children_categories)
                    get(children_categories)
        get(categories)
        all_categories.extend(categories)
        return all_categories

    def show_login(self):
        """
        显示login ui
        :return:
        """
        login_widget = LoginWidget(self)
        login_widget.login_succeed.connect(self.clear)
        login_widget.move_to_center()
        login_widget.exec_()

    def clear(self):
        """
        刷新界面，必须重新选择library
        :return:
        """
        self.category_widget.clear()
        self.tag_widget.clear()
        self.asset_widget.clear()
        # set library
        mliber_global.app().set_value(mliber_library=None)

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
        with mliber_global.db() as db:
            assets = db.find("Asset", filters)
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
            with mliber_global.db() as db:
                tags = db.find("Tag", [["name", "in", tag_names]])
        return tags

    def _on_category_selection_changed(self, categories):
        """
        当category选择改变的时候
        :return:
        """
        all_categories = self._get_children_categories(categories)
        category_ids = [category.id for category in all_categories]
        category_ids = list(set(category_ids))
        with mliber_global.db() as db:
            assets = db.find("Asset", [["category_id", "in", category_ids]])
        self.asset_widget.set_assets(assets)

    def _on_tag_selection_changed(self, tags):
        """
        当tag选择改变的时候
        :return:
        """
        library_assets = []
        if tags:
            assets = list()
            for tag in tags:
                assets.extend(tag.assets)
            if assets:
                library_assets = [asset for asset in assets if asset.library_id == self.library.id]
        else:
            with mliber_global.db() as db:
                library_assets = db.find("Asset", [["library_id", "=", self.library.id]])
        self.asset_widget.set_assets(library_assets)

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
        self.tag_widget.set_tags(tags)

    def _add_tag(self, tag_names):
        """
        当资产添加tag的时候，在tag widget里添加
        :param tag_names: <list>
        :return:
        """
        self.tag_widget.tag_list_view.append_tag(tag_names)

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
                return True
            except RuntimeError as e:
                MessageBox.critical(self, "Login Failed", str(e))
                return False
        return False

    def set_global_library_from_history(self):
        """
        根据历史记录获取library，并设置全局
        :return:
        """
        app = mliber_global.app()
        library_id = mliber_utils.read_history("library_id")
        if library_id:
            with mliber_global.db() as db:
                library = db.find_one("Library",
                                      [["id", "=", library_id],
                                       ["status", "=", "Active"]])
            if library:
                app.set_value(mliber_library=library)
            else:
                app.set_value(mliber_library=None)
            self.refresh_library()

    def _show_create_widget(self):
        """
        show create widget
        :return:
        """
        show_created = False
        if self.library_type and self.category:
            for cls_name, cls in create_widget.classes.iteritems():
                if cls.library_type == self.library_type:
                    widget = cls(parent=self)
                    widget.created_signal.connect(self._create_done)
                    self._add_right_side_widget(widget)
                    show_created = True
                    break
        if not show_created:
            MessageBox.warning(self, "Warning", u"请选择类型.")

    def _create_done(self, assets):
        """
        当创建成功时，返回的已创建的assets
        :param assets:
        :return:
        """
        if not assets:
            return
        asset = assets[0]
        self.asset_widget.asset_list_view.add_asset(assets[0])
        tags = asset.tags
        if not tags:
            return
        tag_names = [tag.name for tag in tags]
        self.tag_widget.tag_list_view.append_tag(tag_names)
        
    def _show_apply(self, assets):
        """
        显示右侧apply widget
        :return: 
        """
        if not assets:
            return
        asset_id = assets[0].id
        with mliber_global.db() as db:
            asset = db.find_one("Asset", [["id", "=", asset_id]])
            apply_widget = ApplyWidget(self)
            apply_widget.set_asset(asset)
            self._add_right_side_widget(apply_widget)

    def _show_right(self):
        """
        显示右边widget
        Returns:
        """
        self.right_widget.setHidden(False)
        self.right_is_shown = True
        self.splitter.setSizes([250, self.width()-500, 250])

    def _add_right_side_widget(self, widget):
        """
        添加右侧widget，要么是preview, 要么是create
        Returns:
        """
        self._show_right()
        count = self.right_stack.count()
        if count == 0:
            self.right_stack.addWidget(widget)
        else:
            for i in xrange(count):
                self.right_stack.takeAt(0)
            self.right_stack.addWidget(widget)

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
