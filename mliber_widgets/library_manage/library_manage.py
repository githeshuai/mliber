from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from library_list_view import LibraryListView
import mliber_resource
from mliber_qt_components.search_line_edit import SearchLineEdit


class LibraryManage(QDialog):
    def __init__(self, parent=None):
        super(LibraryManage, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        # search layout
        search_layout = QHBoxLayout()
        search_layout.addStretch()
        search_layout.setAlignment(Qt.AlignTop)
        self.search_btngrp = QButtonGroup()
        self.name_check_box = QCheckBox("name", self)
        self.name_check_box.setChecked(True)
        self.type_check_box = QCheckBox("type", self)
        self.search_btngrp.addButton(self.name_check_box)
        self.search_btngrp.addButton(self.type_check_box)
        search_layout.addWidget(self.name_check_box)
        search_layout.addWidget(self.type_check_box)
        # search stacked
        self.search_stacked_widget = QStackedWidget(self)
        self.type_combo = QComboBox(self)
        self.search_le = SearchLineEdit(30, 14, self)
        self.search_stacked_widget.addWidget(self.search_le)
        self.search_stacked_widget.addWidget(self.type_combo)
        # add to search layout
        search_layout.addWidget(self.search_stacked_widget)
        # library list view
        self.library_list_view = LibraryListView(self)
        # add to main layout
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.library_list_view)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)
        # set style
        self.set_style()

    def set_style(self):
        """
        set style
        :return:
        """
        self.setStyleSheet(mliber_resource.style())
