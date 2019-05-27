# -*- coding: utf-8 -*-
import os
import sys
import nuke
import nukescripts


mliber_path = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
mliber_path = mliber_path.replace("\\", "/")
site_packages = os.path.join(mliber_path, "mliber_site_packages")
site_packages = site_packages.replace("\\", "/")
sys.path.insert(0, mliber_path)
sys.path.append(site_packages)
from mliber_widgets.main_widget import MainWidget
import mliber
import mliber_resource
liber_menu = nuke.menu("Nodes").addMenu("MLiber", icon=mliber_resource.icon_path("logo.png"))
liber_menu.addCommand("show", mliber.show, "Alt+Q", icon=mliber_resource.icon_path("show.png"))


class MliberWidget(object):
    def __init__(self):
        pass

    def makeUI(self):
        mliber_widget = MainWidget()
        return mliber_widget


class MliberPanel(nukescripts.PythonPanel):
    def __init__(self):
        super(MliberPanel, self).__init__("Mliber", "uk.co.thefoundry.MliberPanel")
        self.mliber_knob = nuke.PyCustom_Knob("Mliber", "", "MliberWidget()")
        self.addKnob(self.mliber_knob)


def add_panel():
    return MliberPanel().addToPane()


menu = nuke.menu('Pane')
menu.addCommand('Mliber', add_panel)
nukescripts.registerPanel('uk.co.thefoundry.MliberPanel', add_panel)
