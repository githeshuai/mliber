# -*- coding: utf-8 -*-
import os
import sys
import nuke
from nukescripts import panels


def add_to_panel():
    property_pane = nuke.getPaneFor('Properties.1')
    my_custom_panel = "uk.co.thefoundry.liber"
    if not nuke.getPaneFor(my_custom_panel):
        pane = panels.registerWidgetAsPanel('LiberWidget', 'LIBER', my_custom_panel, True)
        if property_pane:
            pane.addToPane(property_pane)


liber_path = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
liber_path = liber_path.replace("\\", "/")
if liber_path not in sys.path:
    sys.path.insert(0, liber_path)
from liberScripts.widgets.liberwidget import LiberWidget
import liber
from liberLibs import resource
liber_menu = nuke.menu("Nodes").addMenu("Liber", icon=resource.icon_file("logo.png"))
liber_menu.addCommand("show", liber.show, "Alt+Q", icon=resource.icon_file("show.png"))
liber_menu.addCommand("show in panel", add_to_panel, "Alt+W", icon=resource.icon_file("panel.png"))

