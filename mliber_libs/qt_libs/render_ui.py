# -*- coding: utf-8 -*-
import sys
import contextlib
from Qt.QtWidgets import QApplication


@contextlib.contextmanager
def render_ui():
    """
    show a Qt widget
    :return:
    """
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    yield
    if app:
        sys.exit(app.exec_())
