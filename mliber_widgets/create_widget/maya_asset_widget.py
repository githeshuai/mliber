# -*- coding:utf-8 -*-
import logging
from Qt.QtWidgets import QCheckBox, QWidget, QHBoxLayout
from create_widget import CreateWidget
from mliber_qt_components.input_text_edit import InputTextEdit
from mliber_qt_components.messagebox import MessageBox


class MayaAssetWidget(CreateWidget):
    library_type = "MayaAsset"

    def __init__(self, parent=None):
        super(MayaAssetWidget, self).__init__(self.library_type, parent)
        self.set_engine("maya")
        self.show_thumbnail()
        self.show_common()
        self.show_library_widget()
        self.show_actions()
        self.show_frame_range()
        self.show_progress_bar()
        self.show_create_button()
        self.set_signals()

    def create_library_widget(self):
        """
        继承自基类, checkbox是否导出贴图
        :return:
        """
        widget = QWidget(self)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.export_texture_check = QCheckBox("Export textures", self)
        self.export_texture_check.stateChanged.connect(self.check_state_changed)
        self.recover_check = QCheckBox("Recover after export", self)
        self.export_texture_check.setChecked(True)
        self.recover_check.setChecked(True)
        layout.addWidget(self.export_texture_check)
        layout.addWidget(self.recover_check)
        return widget

    def check_state_changed(self):
        """
        texture check state changed
        :return:
        """
        if self.export_texture:
            self.recover_check.setChecked(True)
        else:
            self.recover_check.setChecked(False)

    @property
    def export_texture(self):
        """
        是否导出贴图
        :return: <bool>
        """
        return self.export_texture_check.isChecked()

    @property
    def recover_texture(self):
        """
        是否还原贴图
        :return:
        """
        return self.recover_check.isChecked()

    def preflight(self):
        """
        重写基类的preflight
        :return:
        """
        if not self.thumbnail_files:
            MessageBox.warning(self, "Warning", "No thumbnail")
            return False
        return True

    def run(self):
        """
        main execute function
        Returns:
        """
        if not self.preflight():
            return
        import maya.cmds as mc
        objects = mc.ls(sl=1)
        text_edit = InputTextEdit(self)
        text_edit.set_title("Selected Nodes")
        text_edit.set_data(objects)
        text_edit.editTextFinished.connect(self.start_create)
        text_edit.exec_()

    def start_create(self, objects):
        """
        :param objects: 需要导出的物体
        :return:
        """
        if not objects:
            MessageBox.warning(self, "Warning", "No objects selected.")
            return
        from mliber_api.maya_asset_maker import MayaAssetMaker
        # database_name, library_id, category_id, asset_name, objects, types = list(), start = 1, end = 1,
        # thumbnail_files = list(), tag_names = list(), description = "", overwrite = True, created_by = None,
        # export_texture = True, recover_texture = True
        data = dict(database_name=self.database,
                    library_id=self.library.id,
                    category_id=self.category.id,
                    asset_name=self.asset_name,
                    objects=objects,
                    types=self.types,
                    start=self.start,
                    end=self.end,
                    thumbnail_files=self.thumbnail_files,
                    tag_names=self.tags,
                    description=self.description,
                    overwrite=self.overwrite,
                    created_by=self.user.id,
                    export_texture=self.export_texture,
                    recover_texture=self.recover_texture)
        self.progress_bar.show()
        self.progress_bar.setRange(0, 10)
        self.progress_bar.setValue(6)
        try:
            maya_asset_maker = MayaAssetMaker(**data)
            asset = maya_asset_maker.make()
            if asset:
                self.created_signal.emit([asset])
        except Exception as e:
            logging.error(str(e))
            MessageBox.warning(None, "Code Error", str(e))
        finally:
            self.progress_bar.setValue(10)
            self.progress_bar.hide()
