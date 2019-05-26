# -*- coding:utf-8 -*-
import logging
from create_widget import CreateWidget
from mliber_qt_components.input_text_edit import InputTextEdit
from mliber_qt_components.messagebox import MessageBox


class MayaAssetWidget(CreateWidget):
    library_type = "MayaShader"

    def __init__(self, parent=None):
        super(MayaAssetWidget, self).__init__(self.library_type, parent)
        self.set_engine("maya")
        self.show_thumbnail()
        self.show_common()
        self.show_actions()
        self.show_progress_bar()
        self.show_create_button()
        self.set_signals()

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
        text_edit.editTextFinished.connect(self._start_create)
        text_edit.exec_()

    def _start_create(self, objects):
        """
        :param objects: 需要导出的物体
        :return:
        """
        if not objects:
            MessageBox.warning(self, "Warning", "No objects selected.")
            return
        from mliber_api.asset_maker import AssetMaker
        # database_name, library_id, category_id, asset_name, objects, types = list(), start = 1, end = 1,
        # thumbnail_files = list(), tag_names = list(), description = "", overwrite = True, created_by = None
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
                    created_by=self.user.id)
        self.progress_bar.show()
        self.progress_bar.setRange(0, 10)
        self.progress_bar.setValue(6)
        try:
            maya_asset_maker = AssetMaker(**data)
            asset = maya_asset_maker.make()
            if asset:
                self.created_signal.emit([asset])
        except Exception as e:
            logging.error(str(e))
            MessageBox.warning(self, "Code Error", str(e))
        finally:
            self.progress_bar.setValue(10)
            self.progress_bar.hide()
