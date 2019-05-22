# -*- coding:utf-8 -*-
from Qt.QtWidgets import QAbstractButton
from Qt.QtCore import Signal
import mliber_global
from lazy_widget_ui import LazyWidgetUI
from mliber_libs.os_libs.path import Path
from mliber_qt_components.messagebox import MessageBox
from mliber_api import asset


class LazyWidget(LazyWidgetUI):
    create_signal = Signal(list)

    def __init__(self, parent=None):
        super(LazyWidget, self).__init__(parent)
        # set signals
        self.set_signals()

    def set_signals(self):
        """
        信号连接
        :return:
        """
        self.batch_check.stateChanged.connect(self._switch_batch_mode)
        self.thumbnail_btn_grp.buttonClicked[QAbstractButton].connect(self._choose_thumbnail)
        self.create_button.clicked.connect(self._create_asset)

    def _switch_batch_mode(self):
        """
        是否batch
        :return:
        """
        if self.batch_check.isChecked():
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(0)

    def _choose_thumbnail(self, button):
        """
        选择缩略图
        :param button:
        :return:
        """
        if button is self.gen_thumbnail_from_file_check:
            self.thumbnail_widget.setHidden(True)
        else:
            self.thumbnail_widget.setHidden(False)

    @property
    def tags(self):
        """
        :return:
        """
        tag_str = self.tag_le.text()
        if tag_str:
            return tag_str.split(",")
        return []

    @property
    def description(self):
        """
        描述
        :return:
        """
        return self.description_te.toPlainText()

    @property
    def overwrite(self):
        """
        :return: <bool>
        """
        return self.overwrite_check.isChecked()

    @property
    def asset_name(self):
        if self.batch_check.isChecked():
            if self._current_files:
                name = Path(self._current_files[0]).filename()
            else:
                name = "NULL"
        else:
            name = self.asset_name_le.text()
        return name

    @property
    def files(self):
        """
        需要上传的文件
        :return: <list>
        """
        return self.files_widget.item_texts()

    @property
    def thumbnail_files(self):
        """
        获取缩略图
        :return: <list>
        """
        if self.gen_thumbnail_from_file_check.isChecked():
            return self._current_files
        else:
            return self.thumbnail_widget.files()

    @property
    def category(self):
        """
        当前选中的category
        :return:
        """
        categories = mliber_global.categories()
        if categories and len(categories) == 1:
            return categories[0]

    @property
    def library(self):
        """
        当前所处的library
        :return:
        """
        return mliber_global.library()

    @property
    def user(self):
        """
        当前登录的用户
        :return:
        """
        return mliber_global.user()

    def _pre_create(self):
        """
        create按钮按下的时候，执行的操作
        :return:
        """
        if not self.user.asset_permission:
            MessageBox.warning(self, "Warning", u"你没有权限创建资产")
            return False
        if not all((self.library, self.category)):
            MessageBox.warning(self, "Warning", u"请先选择类型")
            return False
        if not self.files:
            MessageBox.warning(self, "Warning", u"没有文件可以上传")
            return False
        return True

    def _create_asset(self):
        """
        创建资产
        :return:
        """
        if not self._pre_create():
            return
        database = mliber_global.app().value("mliber_database")
        library_id = self.library.id
        category_id = self.category.id
        created_by = self.user.id
        if self.batch_check.isChecked():
            self._batch_create(database, library_id, category_id, created_by)
        else:
            self._single_create(database, library_id, category_id, created_by)

    def _single_create(self, database, library_id, category_id, created_by):
        """
        :param database: <str>
        :param library_id: <int>
        :param category_id: <int>
        :param created_by: <int>
        :return:
        """
        files = self.files
        self._current_files = files  # 获取缩略图的时候会用到
        if not self.asset_name:
            MessageBox.warning(self, "Warning", u"请填入资产名字")
            return
        ext_list = [Path(f).ext() for f in files]
        ext_list = list(set(ext_list))
        if len(ext_list) > 1:
            MessageBox.warning(self, "Warning", u"只支持相同的格式")
            return
        self.progress_bar.setHidden(False)
        self.progress_bar.setRange(0, 10)
        self.progress_bar.setValue(4)
        asset_instance = asset.Asset(database, library_id, category_id, self.asset_name, files,
                                     self.overwrite, self.description, self.tags, self.thumbnail_files, created_by)
        asset_info = asset_instance.create()
        if asset_info:
            self.create_signal.emit([asset_info])
        self.progress_bar.setValue(10)
        self.progress_bar.setHidden(True)

    def _batch_create(self, database, library_id, category_id, created_by):
        """
        :param database: <str>
        :param library_id: <int>
        :param category_id: <int>
        :param created_by: <int>
        :return:
        """
        self.progress_bar.setHidden(False)
        self.progress_bar.setRange(0, len(self.files))
        for index, source_file in self.files:
            self._current_files = [source_file]  # 获取缩略图的时候会用到
            asset_instance = asset.Asset(database, library_id, category_id, self.asset_name, [source_file],
                                         self.overwrite, self.description, self.tags, self.thumbnail_files, created_by)
            asset_info = asset_instance.create()
            if asset_info:
                self.create_signal.emit([asset_info])
            self.progress_bar.setValue(index + 1)
        self.progress_bar.setHidden(True)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        lw = LazyWidget()
        lw.show()
