# -*- coding: utf-8 -*-
import ix


def undo(func, name="scriptUndo"):
    def _undo(*args, **kwargs):
        ix.begin_command_batch(name)
        result = func(*args, **kwargs)
        ix.end_command_batch()
        return result
    return _undo


def list_children(context, types=list()):
    """
    :param context: clarisse context instance
    :param types: <list>
    :return:
    """
    children = list()
    if types and isinstance(types, basestring):
        types = [types]
    objects = ix.api.OfObjectArray()
    context.get_all_objects("ProjectItem", objects)
    for i in range(objects.get_count()):
        item = objects[i]
        typ = item.get_class().get_name()
        if typ in types:
            children.append(item)
    return children


def geometry_in_context(context):
    """
    geometry in context
    :param context: clarisse context instance
    :return:
    """
    type_list = ["GeometryPolyfile", "GeometryAbcMesh", "AbcXform"]
    children = list_children(context, type_list)
    return children


def texture_in_context(context):
    """
    texture in context
    :param context: clarisse context instance
    :return:
    """
    type_list = ["TextureMapFile"]
    children = list_children(context, type_list)
    return children


def geometry_file_in_context(context):
    """
    geometry files in context
    :param context: clarisse context instance
    :return:
    """
    files = list()
    children = geometry_in_context(context)
    for item in children:
        files.append(item.get_attribute("filename").get_string().replace("\\", "/"))
    return list(set(files))


def create_ibl(hdr_file):
    """
    create ibl
    :param hdr_file: <str> a hdr file path
    :return:
    """
    ix.begin_command_batch("IBLSetupCreate")
    tx = ix.cmds.CreateObject('ibl_tx', 'TextureMapFile')
    tx.attrs.projection = 5
    tx.attrs.filename = str(hdr_file)
    tx.attrs.interpolation_mode = 1
    tx.attrs.mipmap_filtering_mode = 1
    tx.attrs.color_space_auto_detect = False
    tx.attrs.file_color_space = 'linear'
    tx.attrs.pre_multiplied = False
    light = ix.cmds.CreateObject('ibl', 'LightPhysicalEnvironment')
    ix.cmds.SetTexture([light.get_full_name() + ".color"], tx.get_full_name())

    env = ix.cmds.CreateObject('ibl_env', 'GeometrySphere')
    env_mat = ix.cmds.CreateObject('ibl_mat', 'MaterialMatte')
    env.attrs.override_material = env_mat
    env.attrs.unseen_by_camera = True
    env.attrs.cast_shadows = False
    env.attrs.receive_shadows = False
    env.attrs.is_emitter = False
    env.attrs.radius = 500000
    env.attrs.unseen_by_rays = True
    env.attrs.unseen_by_reflections = True
    env.attrs.unseen_by_refractions = True
    env.attrs.unseen_by_gi = True
    env.attrs.unseen_by_sss = True
    ix.cmds.SetTexture([env_mat.get_full_name() + ".color"], tx.get_full_name())
    ix.cmds.SetTexture([light.get_full_name() + ".parent"], env.get_full_name())
    ix.end_command_batch()
