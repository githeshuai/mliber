# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QAction
from Qt.QtCore import Signal
from asset_list_view import AssetListView
from mliber_qt_components.search_line_edit import SearchLineEdit
from mliber_qt_components.indicator_button import ShelfButton
from mliber_qt_components.toolbutton import ToolButton
import mliber_global
from mliber_qt_components.messagebox import MessageBox


class AssetWidget(QWidget):
    export_from_software = Signal()
    create_from_local = Signal()

    def __init__(self, parent=None):
        super(AssetWidget, self).__init__(parent)
        self.assets = []
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # top layout
        top_layout = QHBoxLayout()
        top_layout.setSpacing(0)
        self.asset_btn = ShelfButton("Asset", self)
        self.search_le = SearchLineEdit(25, 12, self)
        self.refresh_btn = ToolButton(self)
        self.refresh_btn.set_size(27, 27)
        self.refresh_btn.set_icon("refresh.png")
        top_layout.addWidget(self.asset_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.search_le)
        top_layout.addWidget(self.refresh_btn)
        # asset list view
        self.asset_list_view = AssetListView(self)
        # add to main layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.asset_list_view)
        # set signals
        self._set_signals()
        # create asset menu
        self._create_asset_menu()

    def _set_signals(self):
        """
        set signals
        :return:
        """
        self.search_le.text_changed.connect(self._filter)

    def set_assets(self, assets):
        """
        接口
        :param assets:
        :return:
        """
        self.assets = assets
        self.asset_list_view.set_assets(assets)
        self.search_le.setText("")
        # set completer
        self.set_completer(self.asset_list_view.asset_names)

    def set_completer(self, asset_list):
        """
        set completer
        :param asset_list:
        :return:
        """
        self.search_le.set_completer(asset_list)

    def _filter(self, filter_str):
        """
        筛选
        :param filter_str:
        :return:
        """
        model = self.asset_list_view.model()
        model.set_filter(filter_str)

    def clear(self):
        """
        清空
        :return:
        """
        model = self.asset_list_view.model()
        if model:
            model.sourceModel().remove_all()
            self.search_le.setText("")

    def _create_asset_menu(self):
        """
        显示asset菜单
        :return:
        """
        self.asset_btn.set_menu()
        self.asset_btn.add_menu_action("Export from software", self._export_from_software)
        self.asset_btn.add_menu_action("Create from local", self._create_from_local)

    def _create_asset(self, mode):
        """
        :param mode: <str> software or local, software means export form software, local means create from local
        :return:
        """
        user = mliber_global.user()
        if not user:
            MessageBox.warning(self, "Warning", "Login First")
            return
        if user.asset_permission:
            if mode == "software":
                self.export_from_software.emit()
            else:
                self.create_from_local.emit()
        else:
            MessageBox.warning(self, "Warning", "Permission denied")

    def _export_from_software(self):
        """
        :return:
        """
        self._create_asset("software")

    def _create_from_local(self):
        """
        :return:
        """
        self._create_asset("local")
