# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
import xgenm
import xgenm.ui as xgui
from mliber_libs.maya_libs.maya_utils import select_objects, get_maya_version, load_plugin, get_scene_name
from mliber_libs.maya_libs.maya_objects import MayaObject


class MayaXgenProxy(MayaObject):
    def __init__(self, path):
        """
        xgen operations
        Args:
            path:
        """
        super(MayaXgenProxy, self).__init__(path)
        self.plugin = "xgenToolkit.mll"

    def export(self, objects, start, end, *args, **kwargs):
        """
        导出xgen代理
        Args:
            objects: 需要导出的物体
            start: <int>
            end: <end>
        Returns:
        """
        if isinstance(objects, basestring):
            objects = [objects]
        directory = os.path.dirname(self.path)
        name = os.path.basename(self.path).split(".")[0]
        if not self.load_plugin():
            return
        if not objects:
            return
        select_objects(objects)
        file_name = get_scene_name()
        hlp = xgenm.xmaya.xgmArchiveExport.xgmArchiveExport()
        version = get_maya_version()
        if version in ["2015"]:
            hlp.processDir(name, directory, [file_name], 0, '0.0', '0.0', start, end)
        else:
            hlp.processDir(name, directory, [file_name], objects, 0, '0.0', '0.0', start, end)
        return self.path

    def import_in(self, *args, **kwargs):
        """
        :return:
        """
        load_plugin(self.plugin)
        xgen_description_editor = xgui.createDescriptionEditor(showIt=False)
        primitive_tab = xgen_description_editor.primitiveTab.widget()
        archive_files_ui = primitive_tab.files
        file_array = [self.path]
        self.addArchives(archive_files_ui, file_array)

    def addArchives(self, archive_files_node, files):
        """
        Add multiple archives from arc files.
        """
        groups = archive_files_node.archiveGroups()
        importedGroups = []
        for f in files:
            with open(f) as fp:
                t = fp.read()
                lines = t.splitlines()
                group = archive_files_node.archiveGroupsFromLines(lines)
                importedGroups.extend(group)
                groups.extend(group)

        if xgenm.xgGlobal.Maya:
            materialFiles = []
            de = xgenm.xgGlobal.DescriptionEditor
            curPal = de.currentPalette()
            curDesc = de.currentDescription()
            for g in importedGroups:
                resolvedMaterials = xgenm.XgExternalAPI.findFileInXgDataPath(str(g.materials), "", curPal, curDesc,
                                                                             "ArchivePrimitive", False, 0, 0, 0)
                if resolvedMaterials and len(resolvedMaterials):
                    materialFiles.append(resolvedMaterials)
            if len(materialFiles):
                strFiles = ""
                for m in materialFiles:
                    strFiles += m + "\n"
                for f in materialFiles:
                    sceneName = os.path.basename(f)
                    sceneExt = os.path.splitext(sceneName)
                    if len(sceneExt[1]):
                        sceneName = sceneExt[0]
                    mc.file(f, i=True, type="mayaAscii", ignoreVersion=True, ra=True, mergeNamespacesOnClash=False,
                            namespace=sceneName, options="v=0;p=17;f=0", pr=True)
        archive_files_node.setArchiveGroups(groups)
