# -*- coding:utf-8 -*-
import sys
import unreal


def init_qt_app():
    unreal.log("MLiber: Initializing QtApp for Unreal")

    from Qt import QtWidgets

    if not QtWidgets.QApplication.instance():
        _qt_app = QtWidgets.QApplication(sys.argv)
        _qt_app.setQuitOnLastWindowClosed(False)
        unreal.log("Created QApplication instance: {0}".format(_qt_app))

        def _app_tick(dt):
            QtWidgets.QApplication.processEvents()

        tick_handle = unreal.register_slate_post_tick_callback(_app_tick)

        def _app_quit():
            unreal.unregister_slate_post_tick_callback(tick_handle)

        QtWidgets.QApplication.instance().aboutToQuit.connect(_app_quit)
    else:
        _qt_app = QtWidgets.QApplication.instance()
