# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QCheckBox, \
    QPushButton, QLabel, QLineEdit, QStackedWidget, QAbstractButton, QTextEdit, QScrollArea, QProgressBar
from Qt.QtCore import Qt, Signal
import mliber_global
from mliber_libs.os_libs.path import Path
from mliber_qt_components.thumbnail_widget import ThumbnailWidget
from mliber_qt_components.drag_file_widget import DragFileWidget
from mliber_qt_components.messagebox import MessageBox
from mliber_api import asset


class LazyWidget(QScrollArea):
    create_signal = Signal(list)

    def __init__(self, parent=None):
        super(LazyWidget, self).__init__(parent)
        self._current_files = []  # 当前正要上传的文件
        widget = QWidget(self)
        self.setWidget(widget)
        self.setWidgetResizable(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # drag file widget
        self.files_widget = DragFileWidget(self)
        # overwrite
        self.overwrite_check = QCheckBox("overwrite", self)
        self.overwrite_check.setChecked(True)
        # tag layout
        tag_layout = QHBoxLayout()
        tag_layout.setContentsMargins(0, 0, 0, 0)
        tag_label = QLabel("Tag", self)
        tag_label.setMaximumWidth(35)
        self.tag_le = QLineEdit(self)
        tag_layout.addWidget(tag_label)
        tag_layout.addWidget(self.tag_le)
        # thumbnail check
        thumbnail_layout = QHBoxLayout()
        self.thumbnail_btn_grp = QButtonGroup()
        self.gen_thumbnail_from_file_check = QCheckBox(u"从文件中生成缩略图", self)
        self.gen_thumbnail_from_file_check.setChecked(True)
        self.upload_thumbnail_check = QCheckBox(u"上传缩略图", self)
        self.thumbnail_btn_grp.addButton(self.gen_thumbnail_from_file_check)
        self.thumbnail_btn_grp.addButton(self.upload_thumbnail_check)
        thumbnail_layout.addWidget(self.gen_thumbnail_from_file_check)
        thumbnail_layout.addWidget(self.upload_thumbnail_check)
        # thumbnail widget
        self.thumbnail_widget = ThumbnailWidget(self)
        self.thumbnail_widget.setHidden(True)
        # stacked widget
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setMaximumHeight(30)
        # asset name widget
        self.asset_name_widget = QWidget(self)
        asset_name_layout = QHBoxLayout(self.asset_name_widget)
        asset_name_layout.setContentsMargins(0, 0, 0, 0)
        asset_name_label = QLabel("name", self)
        asset_name_label.setMaximumWidth(35)
        self.asset_name_le = QLineEdit(self)
        asset_name_layout.addWidget(asset_name_label)
        asset_name_layout.addWidget(self.asset_name_le)
        # add to stacked
        self.stacked_widget.addWidget(self.asset_name_widget)
        self.batch_description_label = QLabel(self)
        self.batch_description_label.setWordWrap(True)
        self.batch_description_label.setText(u"<font color=#ff8c00>批量创建的时候，文件列表中每个文件都会视为一个单独的资产，"
                                             u"且资产名字为文件名。</font>")
        self.stacked_widget.addWidget(self.batch_description_label)
        self.stacked_widget.setMinimumHeight(36)
        # single or batch
        self.batch_check = QCheckBox(u"批量创建", self)
        # description layout
        description_layout = QHBoxLayout()
        description_layout.setContentsMargins(0, 0, 0, 0)
        description_label = QLabel(u"descri\nption", self)
        description_label.setWordWrap(True)
        description_label.setMaximumWidth(33)
        description_label.setAlignment(Qt.AlignTop)
        self.description_te = QTextEdit(self)
        self.description_te.setMaximumHeight(150)
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_te)
        # progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        self.progress_bar.setTextVisible(False)
        # create button
        self.create_button = QPushButton("Create", self)
        # add to main layout
        main_layout.addWidget(self.files_widget)
        main_layout.addWidget(self.overwrite_check)
        main_layout.addLayout(tag_layout)
        main_layout.addLayout(thumbnail_layout)
        main_layout.addWidget(self.thumbnail_widget)
        main_layout.addWidget(self.batch_check)
        main_layout.addWidget(self.stacked_widget)
        main_layout.addLayout(description_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.create_button)
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
            for source_file in self.files:
                self._current_files = [source_file]
                asset_info = asset.create(database, library_id, category_id, self.asset_name, [source_file],
                                          self.overwrite, self.description, self.tags, self.thumbnail_files, created_by)
                if asset_info:
                    self.create_signal.emit([asset_info])


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        lw = LazyWidget()
        lw.show()
