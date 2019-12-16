# -*- coding: utf-8 -*-
import os
import nuke
from Qt.QtWidgets import QApplication


def version():
    """
    获取版本
    :return:
    """
    return "nuke-%s" % nuke.NUKE_VERSION_STRING


def selected_nodes():
    """
    :return: 
    """
    return nuke.selectedNodes()


def export_selected(path):
    """
    :param path: <str>
    :return: 
    """
    _dir = os.path.dirname(path)
    if not os.path.isdir(_dir):
        os.makedirs(_dir)
    nuke.nodeCopy(path)


def nuke_import(path):
    """
    import nuke node for a .nk file
    :param path: <str> 
    :return: 
    """
    nuke.nodePaste(path)


def save_as(path, overwrite=1):
    """
    :param path: <str>
    :param overwrite: 
    :return: 
    """
    file_dir = os.path.dirname(path)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    nuke.scriptSaveAs(path, overwrite=overwrite)


def open_file(file_name):
    """
    open a nuke file
    :param file_name: 
    :return: 
    """
    nuke.scriptClose(ignoreUnsavedChanges=True)
    nuke.scriptOpen(file_name)


def replace_node(old_node, new_node):
    """
    替换节点
    :param old_node: 
    :param new_node: 
    :return: 
    """
    for n in old_node.dependent():
        for i in range(n.inputs()):
            if n.input(i) == old_node:
                n.setInput(i, new_node)
    old_xpos = old_node.xpos()
    old_ypos = old_node.ypos()
    old_node.setXYpos(new_node.xpos(), new_node.ypos())
    new_node.setXYpos(old_xpos, old_ypos)


def parent_window():
    """
    获取父窗口
    :return:
    """
    main_window = None
    app = QApplication.instance()
    for widgets in app.topLevelWidgets():
        if widgets.metaObject().className() == "Foundry::UI::DockMainWindow":
            main_window = widgets
    return main_window
