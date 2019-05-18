# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QAction
from Qt.QtCore import Signal
from asset_list_view import AssetListView
from mliber_qt_components.search_line_edit import SearchLineEdit
from mliber_qt_components.indicator_button import IndicatorButton
import mliber_global


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
        self.asset_btn = IndicatorButton("Asset", self)
        self.search_le = SearchLineEdit(25, 12, self)
        top_layout.addWidget(self.asset_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.search_le)
        # asset list view
        self.asset_list_view = AssetListView(self)
        # add to main layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.asset_list_view)
        # set signals
        self._set_signals()

    def _set_signals(self):
        """
        set signals
        :return:
        """
        self.search_le.text_changed.connect(self._filter)
        self.asset_btn.clicked.connect(self._show_asset_menu)

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
        self.asset_list_view.show_delegate()

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
        menu = QMenu(self)
        export_from_software_action = QAction(u"Export from software", self, triggered=self._export_from_software)
        create_from_local = QAction("Create from local", self, triggered=self._create_from_local)
        menu.addAction(export_from_software_action)
        menu.addAction(create_from_local)
        return menu

    def _show_asset_menu(self):
        """
        显示settings菜单
        :return:
        """
        user = mliber_global.user()
        if user.asset_permission:
            menu = self._create_asset_menu()
            point = self.asset_btn.rect().bottomLeft()
            point = self.asset_btn.mapToGlobal(point)
            menu.exec_(point)

    def _export_from_software(self):
        """
        :return:
        """
        self.export_from_software.emit()

    def _create_from_local(self):
        """
        :return:
        """
        self.create_from_local.emit()
