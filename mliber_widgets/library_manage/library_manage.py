from Qt.QtWidges import *
from Qt.QtGui import *
from Qt.QtCore import *


class LibraryManage(QDialog):
    def __init__(self, parent=None):
        super(LibraryManage, self).__init__(parent)
        main_layout = QVBoxLayout(self)