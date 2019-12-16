# -*- coding: utf-8 -*-
import os
import hou


def selected():
    return hou.selectedNodes()


def version():
    version_str = hou.applicationVersionString()
    return "houdini-%s" % version_str


def parent_win():
    return hou.ui.mainQtWindow()


def create_hda(file_name):
    geo_node = selected()[0]
    if hou.Node.canCreateDigitalAsset(geo_node):
        hda = geo_node.createDigitalAsset(name=geo_node.name(), hda_file_name=file_name, min_num_inputs=0,
                                          max_num_inputs=1, ignore_external_references=True)
        # make sure the spare parameters are stored in the hda as well
        hda_definition = hda.type().definition()
        hda_options = hda_definition.options()
        hda_options.setSaveSpareParms(True)
        hda_definition.setOptions(hda_options)
        hda_definition.save(hda_definition.libraryFilePath(), hda, hda_options)
    else:
        definition = geo_node.type().definition()
        base_name = os.path.basename(os.path.splitext(file_name)[0])
        hou.HDADefinition.copyToHDAFile(definition, file_name, new_name=base_name, new_menu_name=base_name)


def install_hda(file_name):
    hou.hda.installFile(file_name)


def import_abc(abc_path, node_name=None):
    # create geo node
    geo = hou.node("obj").createNode("geo")
    if node_name:
        geo.setName(node_name, 1)
    # delete default file node
    geo_name = geo.name()
    try:
        hou.node("/obj/%s/file1" % geo_name).destroy()
    except:pass
    # create alembic node
    abc_node = geo.createNode("alembic")
    # rename alembic node
    abc_node.setName("%s_alembic" % geo_name)
    # set file name
    abc_node.parm("fileName").set(abc_path)


def save_file(file_path):
    file_dir = os.path.dirname(file_path)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    hou.hipFile.save(file_path)


def open_file(file_path):
    hou.hipFile.load(file_path)


def get_current_network_editor_pane():
    editors = [pane for pane in hou.ui.paneTabs() if isinstance(pane, hou.NetworkEditor) and pane.isCurrentTab()]
    return editors[-1]


def merge_file(file_path):
    hou.hipFile.merge(file_path, ignore_load_warnings=True)
