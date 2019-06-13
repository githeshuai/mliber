# -*- coding: utf-8 -*-
import sys
import time
from Qt.QtWidgets import QApplication, QSplashScreen
from Qt.QtCore import Qt, QCoreApplication
from Qt.QtGui import QPixmap
import mliber_resource


def splash(func):
    def _wrapper(*args, **kwargs):
        # display exit splash screen
        sys_app = None
        app = QApplication.instance()
        if not app:
            sys_app = QApplication(sys.argv)
        pixmap_path = mliber_resource.pixmap("splash.png")
        splash_pix = QPixmap(pixmap_path)
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        start = time.time()
        QCoreApplication.processEvents()
        result = func(*args, **kwargs)
        splash.finish(result)
        splash.raise_()
        if sys_app:
            sys_app.exec_()
        return result
    return _wrapper
