from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from library_list_view import LibraryListView


class LibraryManage(QDialog):
    def __init__(self, parent=None):
        super(LibraryManage, self).__init__(parent)
        main_layout = QVBoxLayout(self)

        self.library_list_view = LibraryListView(self)
        main_layout.addWidget(self.library_list_view)

        self.button = QPushButton("test")
        self.button.clicked.connect(self.get_selected)
        main_layout.addWidget(self.button)

    def get_selected(self):
        print self.library_list_view.selectedIndexes()