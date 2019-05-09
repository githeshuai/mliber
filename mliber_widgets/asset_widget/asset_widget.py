# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout
from asset_list_view import AssetListView
import mliber_resource


class AssetWidget(QWidget):
    def __init__(self, parent=None):
        super(AssetWidget, self).__init__(parent)
        self.assets = None
        main_layout = QVBoxLayout(self)
        self.asset_list_view = AssetListView(self)
        main_layout.addWidget(self.asset_list_view)

    def set_assets(self, assets):
        self.assets = assets
        self.asset_list_view.set_assets(assets)
