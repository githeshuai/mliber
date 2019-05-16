# -*- coding: utf-8 -*-
import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import maya.utils as mu
from Qt import __binding__
from Qt.QtCore import *
from Qt.QtWidgets import *


def get_scene_name():
    """
    get scene name
    Returns:
    """
    return pm.system.sceneName()


def plugin_loaded(plugin):
    """
    check plugin is loaded
    :param plugin:
    :return:
    """
    return mc.pluginInfo(plugin, q=1, loaded=1)


def load_plugin(plugin):
    """
    load plugin
    :param plugin: plugin name
    :return: if loaded return True else False
    """
    if not plugin_loaded(plugin):
        try:
            mc.loadPlugin(plugin, quiet=1)
            return True
        except:
            return False
    return True


def get_file_type(path):
    """
    get file tpye
    Args:
        path: <str>

    Returns:

    """
    file_type = None
    if path.endswith(".abc"):
        file_type = "Alembic"
    elif path.endswith(".mb"):
        file_type = "mayaBinary"
    elif path.endswith(".ma"):
        file_type = "mayaAscii"
    elif path.endswith(".fbx"):
        file_type = "Fbx"
    elif path.endswith(".obj"):
        file_type = "OBJexport"
    return file_type


def create_reference(path, namespace_name=":", allow_repeat=False, get_group=False):
    """
    create reference
    Args:
        path: <str> maya file
        namespace_name: <str> namespace
        allow_repeat: <bool>
        get_group: <bool> whether get the reference group in maya outliner

    Returns:
        if get_group return group name in outliner else None
    """
    result = None
    path = path.replace("\\", "/")
    if path.endswith(".abc"):
        load_plugin("AbcImport.mll")
    file_type = get_file_type(path)
    if allow_repeat:
        result = pm.system.createReference(path, loadReferenceDepth="all",
                                           mergeNamespacesOnClash=False,
                                           namespace=namespace_name,
                                           type=file_type)
    else:
        references = pm.listReferences()
        if not references:
            print "*" * 100
            result = pm.system.createReference(path, loadReferenceDepth="all",
                                               ignoreVersion=1, gl=1,
                                               options="v=0",
                                               mergeNamespacesOnClash=True,
                                               namespace=namespace_name,
                                               type=file_type)
        else:
            reference_paths = [ref.path for ref in references]
            if path not in reference_paths:
                result = pm.system.createReference(path, loadReferenceDepth="all",
                                                   mergeNamespacesOnClash=True,
                                                   namespace=namespace_name,
                                                   type=file_type)
            else:
                ref_node = pm.referenceQuery(path, referenceNode=1)
                if not pm.referenceQuery(ref_node, isLoaded=1):
                    pm.system.loadReference(path)
    if get_group:
        return pm.referenceQuery(result.refNode, dagPath=1, nodes=1)[0]


def get_frame_padding():
    """
    get maya render setting frame padding
    Returns: int
    """
    return mc.getAttr("defaultRenderGlobals.extensionPadding")


def get_maya_version():
    """
    get maya version
    Returns: <str> maya version
    """
    version = mc.about(v=1)
    return "Maya_%s" % version


def get_plugin_version(plugin_name):
    """
    Args:
        plugin_name: <str> plugin name
    Returns: <str> if plugin is loaded return plugin version else None
    """
    if plugin_loaded(plugin_name):
        version = mc.pluginInfo(plugin_name, q=1, v=1)
        return "{} {}".format(plugin_name.split(".")[0], version)
    return None


def select_objects(objects):
    """
    选中物体
    Args:
        objects:
    Returns:

    """
    mc.select(objects, r=1)


def post_export_textures(temp_dict):
    """
    recover the texture node's value
    Args:
        temp_dict:
    Returns:

    """
    if temp_dict:
        for attr in temp_dict:
            if temp_dict.get(attr):
                mc.setAttr(attr, temp_dict.get(attr), type="string")


def get_maya_win(module="PySide"):
    """
    get a QMainWindow Object of maya main window
    :param module (optional): string "PySide"(default) or "PyQt4"
    :return main_window: QWidget or QMainWindow object
    """
    import maya.OpenMayaUI as mui
    prt = mui.MQtUtil.mainWindow()
    if module == "PyQt":
        import sip
        main_window = sip.wrapinstance(long(prt), QObject)
    elif module in ["PySide"]:
        if __binding__ in ["PySide"]:
            import shiboken
        elif __binding__ in ["PySide2"]:
            import shiboken2 as shiboken
        main_window = shiboken.wrapInstance(long(prt), QWidget)
    elif module == "mayaUI":
        main_window = "MayaWindow"
    else:
        raise ValueError('param "module" must be "mayaUI" "PyQt4" or "PySide"')
    return main_window


def show_as_panel(widget_instance, title=None):
    if not isinstance(widget_instance, QWidget):
        raise ValueError("%s is not a Qt Widget." % widget_instance)

    obj_name = widget_instance.objectName()
    # parent current dialog to maya win
    maya_main_window = get_maya_win()
    widget_instance.setParent(maya_main_window)
    # dock the panel on maya
    if not title:
        title = widget_instance.windowTitle() or widget_instance.objectName()
    dock_panel(obj_name, widget_instance, title)

    return widget_instance


def dock_panel(object_name, widget_instance, title):
    maya_panel_name = "panel_%s" % object_name
    # delete existed panel
    if mc.control(maya_panel_name, query=True, exists=True):
        mc.deleteUI(maya_panel_name)

    if int(str(mc.about(api=True))[:4]) < 2017:

        # Create a new Maya window.
        maya_window = mc.window()

        # Add a layout to the Maya window.
        maya_layout = mc.formLayout(parent=maya_window)

        # Reparent the Shotgun app panel widget under the Maya window layout.
        mc.control(object_name, edit=True, parent=maya_layout)

        # Keep the Shotgun app panel widget sides aligned with the Maya window layout sides.
        mc.formLayout(maya_layout,
                      edit=True,
                      attachForm=[(object_name, 'top', 1),
                                  (object_name, 'left', 1),
                                  (object_name, 'bottom', 1),
                                  (object_name, 'right', 1)])

        # Dock the Maya window into a new tab of Maya Channel Box dock area.
        mc.dockControl(maya_panel_name, area="right", content=maya_window, label=title)

        # Once Maya will have completed its UI update and be idle,
        # raise (with "r=True") the new dock tab to the top.
        mu.executeDeferred("cmds.dockControl('%s', edit=True, r=True)" % maya_panel_name)

    else:  # Maya 2017 and later
        # Delete any default workspace control state that might have been automatically
        # created by Maya when a previously existing Maya panel was closed and deleted.
        if mc.workspaceControlState(maya_panel_name, exists=True):
            mc.workspaceControlState(maya_panel_name, remove=True)

        # Retrieve the Channel Box dock area, with error reporting turned off.
        # This MEL function is declared in Maya startup script file UIComponents.mel.
        # It returns an empty string when this dock area cannot be found in the active Maya workspace.
        dock_area = mel.eval('getUIComponentDockControl("Channel Box / Layer Editor", false)')

        # This UI script will be called to build the UI of the new dock tab.
        # It will embed the Shotgun app panel widget into a Maya workspace control.
        # Maya 2017 expects this script to be passed in as a string, not as a function pointer.
        # See function _build_workspace_control_ui() below for a commented version of this script.
        ui_script = "import pymel.core as pm\n" \
                    "workspace_control = pm.setParent(query=True)\n" \
                    "pm.control('%s', edit=True, parent=workspace_control)" \
                    % object_name

        # The following UI script can be used for development and debugging purposes.
        # This script has to retrieve and import the current source file in order to call
        # function _build_workspace_control_ui() below to build the workspace control UI.
        # ui_script = "import imp\n" \
        #             "panel_generation = imp.load_source('%s', '%s')\n" \
        #             "panel_generation._build_workspace_control_ui('%s')" \
        #             % (__name__, __file__.replace(".pyc", ".py"), object_name)

        # Give an initial width to the docked Shotgun app panel widget when first shown.
        # Otherwise, the workspace control would use the width of the currently displayed tab.
        size_hint = widget_instance.sizeHint()
        if size_hint.isValid():
            # Use the widget layout preferred size.
            widget_width = size_hint.width()
        else:
            # Since no size is recommended for the widget, use its current width.
            widget_width = widget_instance.width()

        # Dock the Shotgun app panel widget into a new tab of the Channel Box dock area.
        # When this dock area was not found in the active Maya workspace,
        # the Shotgun app panel widget is embedded into a floating workspace control window.
        # This floating workspace control can then be docked into an existing dock area by the user.
        dock_tab = mc.workspaceControl(maya_panel_name,
                                       tabToControl=(dock_area, -1),  # -1 to append a new tab
                                       uiScript=ui_script,
                                       loadImmediately=True,
                                       retain=False,  # delete the dock tab when it is closed
                                       label=title,
                                       initialWidth=widget_width,
                                       minimumWidth=True,  # set the minimum width to the initial width
                                       r=True  # raise the new dock tab to the top
                                       )

        # Now that the workspace dock tab has been created, let's update its UI script.
        # This updated script will be saved automatically with the workspace control state
        # in the Maya layout preference file when the user will choose to quit Maya,
        # and will be executed automatically when Maya is restarted later by the user.

        # The script will delete the empty workspace dock tab that Maya will recreate on startup
        # when the user previously chose to quit Maya while the panel was opened.
        deferred_script = "import maya.cmds as cmds\\n" \
                          "if cmds.workspaceControl('%(id)s', exists=True):\\n" \
                          "    cmds.deleteUI('%(id)s')" \
                          % {"id": maya_panel_name}

        # The previous script will need to be executed once Maya has completed its UI update and be idle.
        ui_script = "import maya.utils\n" \
                    "maya.utils.executeDeferred(\"%s\")\n" \
                    % deferred_script

        # Update the workspace dock tab UI script.
        mc.workspaceControl(maya_panel_name, edit=True, uiScript=ui_script)
