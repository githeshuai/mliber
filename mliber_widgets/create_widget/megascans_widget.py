#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-12-03 11:10
# Author    : Mr. He
# Version   :
# Usage     : 
# Notes     :

# Import built-in modules

# Import third-party modules
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
# Import local modules
from mliber_qt_components.messagebox import MessageBox
from mliber_qt_components.action_widget import ActionWidget
from mliber_qt_components.drag_file_widget import DragFileWidget
from mliber_qt_components.info_dialog import InfoWidget
from mliber_libs.megascans_libs.megascans_asset import MegascansAsset
from mliber_libs.os_libs.path import Path
import mliber_global
from mliber_api.asset_maker import AssetMaker


class MayaWidget(QWidget):
    def __init__(self, parent=None):
        super(MayaWidget, self).__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        # form layout
        form_layout = QFormLayout()
        self._maya_path_le = QLineEdit(self)
        self._maya_path_le.setPlaceholderText("mayapy path here")
        self._renderer_combo = QComboBox(self)
        self._renderer_combo.addItems(["Arnold", "Redshift", "Vray"])
        self._render_plugin_le = QLineEdit(self)
        self._render_plugin_le.setPlaceholderText(".mll or .so plugin file here")
        self._lod_combo = QComboBox(self)
        self._lod_combo.addItems(["LOD0", "LOD1", "LOD2", "LOD3", "LOD4", "LOD5"])
        self._resolution_combo = QComboBox(self)
        self._resolution_combo.addItems(["8K", "4K", "2K", "1K"])
        form_layout.addRow("mayapy path", self._maya_path_le)
        form_layout.addRow("Renderer", self._renderer_combo)
        form_layout.addRow("Renderer Plugin", self._render_plugin_le)
        form_layout.addRow("Lod", self._lod_combo)
        form_layout.addRow("Resolution", self._resolution_combo)
        # action widget
        self._action_widget = ActionWidget("Megascans", "maya", self)
        # add to main
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self._action_widget)


class MegascansWidget(QWidget):
    created_signal = Signal(list)

    def __init__(self, parent=None):
        super(MegascansWidget, self).__init__(parent)
        self._setup_ui()
        self._set_signals()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        # drag file widget
        self._file_list = DragFileWidget(self)
        self._file_list.set_filter(["json"])
        # check button group
        check_btn_layout = QHBoxLayout()
        self.button_group = QButtonGroup()
        self._only_copy_btn = QCheckBox("Only Copy", self)
        self._maya_btn = QCheckBox("Resolve in Maya", self)
        for index, btn in enumerate([self._only_copy_btn, self._maya_btn]):
            btn.index = index
            check_btn_layout.addWidget(btn)
            self.button_group.addButton(btn)
        # stacked widget
        self.stacked_widget = QStackedWidget(self)
        null_widget = QWidget(self)
        maya_widget = MayaWidget(self)
        self.stacked_widget.addWidget(null_widget)
        self.stacked_widget.addWidget(maya_widget)
        # info widget
        detail_group = QGroupBox("Detail")
        detail_layout = QHBoxLayout(detail_group)
        detail_layout.setContentsMargins(0, 0, 0, 0)
        self.info_widget = InfoWidget(self)
        self.info_widget.set_button_shown(False)
        detail_layout.addWidget(self.info_widget)
        # create button
        self.create_btn = QPushButton("Create", self)
        # add to main
        main_layout.addWidget(self._file_list)
        main_layout.addLayout(check_btn_layout)
        main_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(detail_group)
        main_layout.addWidget(self.create_btn)

    def _set_signals(self):
        """
        set signals
        :return:
        """
        self.button_group.buttonClicked[QAbstractButton].connect(self._switch_stack)
        self.create_btn.clicked.connect(self._create_asset)

    def _switch_stack(self, button):
        """
        :return:
        """
        index = button.index
        self.stacked_widget.setCurrentIndex(index)

    @property
    def json_files(self):
        """
        列表里所有的json文件
        :return:
        """
        return self._file_list.item_texts()

    @property
    def mode(self):
        """
        是only copy还是resolve in maya
        :return:
        """
        if self.stacked_widget.currentIndex() == 0:
            return "only_copy"
        elif self.stacked_widget.currentIndex() == 1:
            return "resolve in maya"

    def _crete_with_only_copy(self):
        """
        仅仅只是拷贝的情况
        :return:
        """
        # database_name, library_id, category_id, asset_name, objects, types, start=1, end=1,
        # thumbnail_files=list(), tag_names=list(), description="", overwrite=True, created_by=None, source=None
        user = mliber_global.user()
        if not user.asset_permission:
            MessageBox.warning("self", "Warning", "Permission denied !")
            return
        database_name = mliber_global.database()
        library_id = mliber_global.library().id
        category_id = mliber_global.categories()[0].id
        user_id = mliber_global.user().id
        types = ["megascans"]
        self.info_widget.set_progress_range(0, len(self.json_files))
        for index, json_file in enumerate(self.json_files):
            asset_dir = Path(json_file).parent()
            asset = MegascansAsset(asset_dir)
            tags = asset.tags()
            asset_name = asset.name()
            thumbnail = asset.thumbnail()
            asset_maker = AssetMaker(database_name, library_id, category_id, asset_name, objects=None, types=types,
                                     thumbnail_files=thumbnail, tag_names=tags, created_by=user_id, source=asset_dir)
            try:
                asset = asset_maker.make()
                if asset:
                    self.created_signal.emit([asset])
                self.info_widget.append_pass("%s publish completed" % asset_name)
            except RuntimeError as e:
                self.info_widget.append_error(str(e))
                self.info_widget.append_error("%s publish failed" % asset_name)
            self.info_widget.set_progress_value(index+1)

    def _create_asset(self):
        """
        :return:
        """
        if self.mode == "only_copy":
            self._crete_with_only_copy()
