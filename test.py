from Qt.QtWidgets import QDialog, QPushButton, QHBoxLayout
from mliber_api.database_api import Database


class TestWidget(QDialog):
    def __init__(self, parent=None):
        super(TestWidget, self).__init__(parent)

        layout = QHBoxLayout(self)
        btn = QPushButton("test", self)
        layout.addWidget(btn)
        btn.clicked.connect(self.test)

    def test(self):
        db = Database()
        print db.find("User", [])


from mliber_libs.qt_libs import render_ui
with render_ui.render_ui():
    tw = TestWidget()
    tw.show()
