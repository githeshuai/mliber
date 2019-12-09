#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-12-03 11:10
# Author    : Mr. He
# Version   :
# Usage     : 
# Notes     :

# Import built-in modules
import subprocess
# Import third-party modules
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
# Import local modules
from mliber_qt_components.messagebox import MessageBox
from mliber_qt_components.action_widget import ActionWidget
from mliber_qt_components.drag_file_widget import DragFileWidget
from mliber_qt_components.info_dialog import InfoWidget
from mliber_libs.megascans_libs.megascans_asset import MegascansAsset
from mliber_libs.os_libs.path import Path
import mliber_global
import mliber_utils
from mliber_api.asset_maker import AssetMaker
from mliber_custom import MAYA_VERSION_MAPPING, RENDERER_MAPPING


class MayaWidget(QWidget):
    def __init__(self, parent=None):
        super(MayaWidget, self).__init__(parent)
        self._setup_ui()
        self._set_signals()
        self._init()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # form layout
        form_layout = QFormLayout()
        self._maya_path_combo = QComboBox(self)
        self._renderer_combo = QComboBox(self)
        self._renderer_combo.addItems(["Arnold", "Redshift", "Vray"])
        self._render_plugin_combo = QComboBox(self)
        self._lod_combo = QComboBox(self)
        self._lod_combo.addItems(["LOD0", "LOD1", "LOD2", "LOD3", "LOD4", "LOD5"])
        self._resolution_combo = QComboBox(self)
        self._resolution_combo.addItems(["8K", "4K", "2K", "1K"])
        form_layout.addRow("mayapy path", self._maya_path_combo)
        form_layout.addRow("Renderer", self._renderer_combo)
        form_layout.addRow("Renderer Plugin", self._render_plugin_combo)
        form_layout.addRow("Lod", self._lod_combo)
        form_layout.addRow("Resolution", self._resolution_combo)
        # action widget
        self._action_widget = ActionWidget("Megascans", "maya", self)
        # texture widget
        texture_layout = QHBoxLayout()
        texture_layout.setContentsMargins(0, 0, 0, 0)
        self.export_texture_check = QCheckBox("Export textures", self)
        self.export_texture_check.setChecked(True)
        texture_layout.addWidget(self.export_texture_check)
        # add to main
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self._action_widget)
        main_layout.addLayout(texture_layout)

    def _set_signals(self):
        """
        set signals
        :return:
        """
        self._renderer_combo.currentIndexChanged.connect(self._switch_renderer)

    def _switch_renderer(self):
        """
        切换渲染器
        :return:
        """
        renderer = self.renderer
        render_versions = RENDERER_MAPPING.get(renderer, {}).keys()
        self._render_plugin_combo.clear()
        self._render_plugin_combo.addItems(render_versions)

    def _init(self):
        """
        initialize
        :return:
        """
        self._maya_path_combo.addItems(MAYA_VERSION_MAPPING.keys())
        self._switch_renderer()

    @property
    def maya_py(self):
        """
        get maya py path
        :return:
        """
        maya_version = self._maya_path_combo.currentText()
        return MAYA_VERSION_MAPPING.get(maya_version)

    @property
    def renderer(self):
        """
        get renderer
        :return:
        """
        return self._renderer_combo.currentText()

    @property
    def renderer_plugin_path(self):
        """
        get renderer plugin path
        :param self:
        :return:
        """
        renderer_version = self._render_plugin_combo.currentText()
        return RENDERER_MAPPING.get(self.renderer, {}).get(renderer_version)

    @property
    def lod(self):
        """
        get current LOD
        :param self:
        :return:
        """
        return self._lod_combo.currentText()

    @property
    def resolution(self):
        """
        get current resolution
        :return:
        """
        return self._resolution_combo.currentText()

    @property
    def types(self):
        """
        get selected element types
        :return:
        """
        buttons = self._action_widget.checked_buttons()
        types = [button.type for button in buttons]
        return types

    @property
    def export_texture(self):
        """
        是否导出贴图
        :return: <bool>
        """
        return self.export_texture_check.isChecked()


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
        self.maya_widget = MayaWidget(self)
        self.stacked_widget.addWidget(null_widget)
        self.stacked_widget.addWidget(self.maya_widget)
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

    @staticmethod
    def _get_job_file():
        """
        get job megascans to maya file
        :return:
        """
        jobs_dir = mliber_utils.package("mliber_jobs")
        return Path(jobs_dir).join("job_megascans_to_maya.py")

    def _validate_resolve_in_maya(self):
        """
        validate resolve in maya
        :return:
        """
        categories = mliber_global.categories()
        if not categories:
            MessageBox.warning(self, "Warning", "Select one category first.")
            return False
        maya_py_path = self.maya_widget.maya_py
        if not Path(maya_py_path).isfile():
            MessageBox.warning(self, "Warning", "Mayapy %s is not an exist file." % maya_py_path)
            return False
        render_plugin_path = self.maya_widget.renderer_plugin_path
        if not Path(render_plugin_path).isfile():
            MessageBox.warning(self, "Warning", "Renderer %s is not an exist file." % maya_py_path)
            return False
        return True

    def _resolve_in_maya(self):
        """
        自动生成maya文件
        :return:
        """
        job_file = self._get_job_file()
        # get data
        database_name = mliber_global.database()
        library_id = mliber_global.library().id
        category_id = mliber_global.categories()[0].id
        types = self.maya_widget.types
        renderer_plugin_path = self.maya_widget.renderer_plugin_path
        lod = self.maya_widget.lod
        resolution = self.maya_widget.resolution
        renderer = self.maya_widget.renderer
        export_texture = self.maya_widget.export_texture
        created_by = mliber_global.user().id
        self.info_widget.set_progress_range(0, len(self.json_files))
        for index, json_file in enumerate(self.json_files):
            asset_dir = Path(json_file).parent()
            cmd = [self.maya_widget.maya_py, job_file, database_name, str(library_id), str(category_id), asset_dir,
                   ",".join(types), renderer_plugin_path, lod, resolution, renderer,
                   str(export_texture), "True", str(created_by)]
            sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            while True:
                return_code = sp.poll()
                if return_code == 0:
                    break
                elif return_code == 1:
                    command_info = "%s was terminated for some reason." % cmd
                    self.info_widget.append_error(command_info)
                    break
                elif return_code is not None:
                    command_info = "exit return code is: %s" % str(return_code)
                    self.info_widget.append_error(command_info)
                    break
                line = sp.stdout.readline()
                line = line.strip()
                if line:
                    self.info_widget.append_info(line)
            self.info_widget.set_progress_value(index + 1)

    def _create_asset(self):
        """
        :return:
        """
        self.info_widget.clear()
        if self.mode == "only_copy":
            self._crete_with_only_copy()
        elif self.mode == "resolve in maya":
            if self._validate_resolve_in_maya():
                self._resolve_in_maya()
