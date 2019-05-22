# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QCheckBox, \
    QPushButton, QLabel, QLineEdit, QStackedWidget, QAbstractButton, QTextEdit, QScrollArea, QProgressBar
from Qt.QtCore import Qt
from mliber_qt_components.thumbnail_widget import ThumbnailWidget
from mliber_qt_components.drag_file_widget import DragFileWidget


class LazyWidgetUI(QScrollArea):
    def __init__(self, parent=None):
        super(LazyWidgetUI, self).__init__(parent)
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
        self.progress_bar.setHidden(True)
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
