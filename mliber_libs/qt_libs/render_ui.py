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
    app = None
    is_app_running = QApplication.instance()
    if not is_app_running:
        app = QApplication(sys.argv)
    yield
    if app:
        sys.exit(app.exec_())
