# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from asset_list_view import AssetListView
from mliber_qt_components.search_line_edit import SearchLineEdit


class AssetWidget(QWidget):
    def __init__(self, parent=None):
        super(AssetWidget, self).__init__(parent)
        self.assets = []
        main_layout = QVBoxLayout(self)
        # top layout
        top_layout = QHBoxLayout()
        self.asset_btn = QPushButton("Asset", self)
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
        self.set_signals()

    def set_signals(self):
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
