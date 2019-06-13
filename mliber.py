# -*- coding: utf-8 -*-
import os
import sys


mliber_path = os.path.dirname(__file__)
mliber_path = mliber_path.replace("\\", "/")
site_packages = os.path.join(mliber_path, "mliber_site_packages")
site_packages = site_packages.replace("\\", "/")
if mliber_path not in sys.path:
    sys.path.insert(0, mliber_path)
if site_packages not in sys.path:
    sys.path.append(site_packages)

from mliber_libs.qt_libs.render_ui import render_ui
from mliber_libs.dcc_libs.dcc import Dcc
from mliber_widgets.main_widget import MainWidget
from mliber_qt_components.splash import splash


PARENT_WINDOW = Dcc().parent_win()


# ######################################################################################
# ##################################### show standalone ################################
# ######################################################################################
@splash
def show():
    with render_ui():
        mliber_widget = MainWidget(PARENT_WINDOW)
        mliber_widget.show()
        return mliber_widget


# ######################################################################################
# ##################################### show in maya ###################################
# ######################################################################################
def show_in_maya_panel(*args):
    """
    show in maya panel
    :param args:
    :return:
    """
    from mliber_libs.maya_libs.maya_utils import show_as_panel
    show_as_panel(MainWidget())


def show_in_maya():
    """
    add menu in maya, and make the command connections
    :return:
    """
    import maya.cmds as mc
    import mliber
    liber_menu = mc.menu('mliber', label="MLiber", tearOff=True, parent='MayaWindow')
    mc.menuItem(label="Show...", tearOff=True, parent=liber_menu, c=lambda *args: mliber.show())
    mc.menuItem(label="show in panel...", tearOff=True, parent=liber_menu, c=mliber.show_in_maya_panel)


def maya_start_up():
    """
    when maya start up, execute.
    :return:
    """
    import maya.utils as mu
    mu.executeDeferred("import mliber;reload(mliber);mliber.show_in_maya()")


# ######################################################################################
# ##################################### show in houdini ################################
# ######################################################################################
def show_in_houdini():
    show()


if __name__ == "__main__":
    show()




