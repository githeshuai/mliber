# -*- coding: utf-8 -*-
import os
import re
import logging
import ix
from mliber_hook.base_hook import BaseHook
from mliber_libs.clarisse_libs import clarisse_utils
from mliber_libs.os_libs.path import Path


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self, *args, **kwargs):
        sels = ix.selection
        if sels.get_count() == 1:
            context = sels[0]
            if context.is_context():
                ix.begin_command_batch("ContextExport")
                # export geo
                geos = clarisse_utils.geometry_in_context(context)
                geo_assembly = self._assembly(geos, "geo")
                self._export_geos(geo_assembly)
                # export texture
                textures = clarisse_utils.texture_in_context(context)
                texture_assembly = self._assembly(textures, "texture")
                self._export_textures(texture_assembly)
                # export context
                ix.export_context_as_project(context, str(self.path))
                # recover assembly
                assemblies = geo_assembly + texture_assembly
                for assembly in assemblies:
                    assembly.get("node").attrs.filename = str(assembly.get("old"))
                ix.end_command_batch()
                return self.path
            else:
                self.append_error("Only context support.")
        else:
            self.append_error("Only one context support.")

    @staticmethod
    def _export_geos(geo_assembly):
        """
        export geometry
        :param geo_assembly: <list> list of dict
        :return: 
        """
        for i in geo_assembly:
            node = i.get("node")
            old = str(i.get("old"))
            new = str(i.get("new"))
            new_path = os.path.join(os.path.dirname(new), os.path.basename(old)).replace("\\", "/")
            if os.path.isfile(old):
                Path(old).copy_to(new_path)
                ix.cmds.SetValues(["%s.filename[0]" % str(node)], [new_path])

    def _export_textures(self, texture_assembly):
        for i in texture_assembly:
            node = i.get("node")
            old = str(i.get("old"))
            new = str(i.get("new"))
            old_textures = self._get_texture_abs_path(old)
            for texture in old_textures:
                if os.path.isfile(texture):
                    new_path = os.path.join(os.path.dirname(new), os.path.basename(texture)).replace("\\", "/")
                    Path(texture).copy_to(new_path)
                    ix.cmds.SetValues(["%s.filename[0]" % str(node)], [new])
    
    def _export_context_as_project(self):
        return
    
    def _assembly(self, nodes, typ):
        """
        几何体和贴图描述
        :param nodes: clarisse node list
        :param typ: <str>
        :return: 
        """
        resolution = list()
        node_dir = Path(self.path).parent() + "/" + typ
        for node in nodes:
            temp_dict = dict()
            filename = node.get_attribute("filename").get_string().replace("\\", "/")
            if not filename:
                continue
            basename = Path(filename).basename()
            new_file_name = os.path.join(node_dir, basename).replace("\\", "/")
            temp_dict["node"] = node
            temp_dict["old"] = filename
            temp_dict["new"] = new_file_name
            resolution.append(temp_dict)
        return resolution
    
    @staticmethod
    def _get_texture_abs_path(texture):
        real_texture = list()
        if not texture:
            return []
        texture = texture.replace("\\", "/")
        if texture.startswith("$"):
            _list = texture.split("/")
            prefix = _list[0]
            env = prefix.split("$")[-1]
            env = env.strip("{").strip("}")
            suffix = "/".join(_list[1:])
            env_path = os.environ.get(env)
            if not env_path:
                return []
            texture = "{0}/{1}".format(env_path, suffix)
        if "<udim>" in texture or "<UDIM>" in texture:
            texture_dir, texture_base_name = os.path.split(texture)
            pattern = texture_base_name.replace("<udim>", "\d{4}")
            pattern = pattern.replace("<UDIM>", "\d{4}")
            if os.path.isdir(texture_dir):
                for i in os.listdir(texture_dir):
                    if re.match(pattern, i):
                        full_name = "%s/%s" % (texture_dir, i)
                        full_name = full_name.replace("\\", "/")
                        real_texture.append(full_name)
        elif os.path.isfile(texture):
            real_texture.append(texture)
        else:
            logging.warning("%s is not an exist file." % texture)
        return real_texture
