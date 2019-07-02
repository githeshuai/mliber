# -*- coding:utf-8 -*-
"""
资产的导入，包括Texture, Static Mesh, Skeleton, Animation
"""
import unreal


def build_import_task(filename, destination_path, destination_name="", options=None):
    """
    创建导入资产task
    :param filename: <str> 需要导入的资产名字
    :param destination_path: <str> 导入之后在content中的路径
    :param destination_name: <str> 导入资产后节点的名字
    :param options:
    :return:
    """
    task = unreal.AssetImportTask()
    task.set_editor_property("automated", True)  # 是否需要显示ui
    task.set_editor_property("destination_name", destination_name)
    task.set_editor_property("destination_path", destination_path)
    task.set_editor_property("filename", filename)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)
    if options:
        task.set_editor_property("options", options)
    return task


def build_static_mesh_import_options(materials=True, textures=True):
    """
    导入static mesh
    :param materials: <bool> 是否导入材质球
    :param textures: <bool> 是否导入贴图
    :return:
    """
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_textures", textures)
    options.set_editor_property("import_materials", materials)
    options.set_editor_property("import_as_skeletal", False)
    # unreal.FbxMeshImportData
    options.static_mesh_import_data.set_editor_property("import_translation", unreal.Vector(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property("import_rotation", unreal.Rotator(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property("import_uniform_scale", 1.0)
    # unreal.FbxStaticMeshImportData
    options.static_mesh_import_data.set_editor_property("combine_meshes", True)
    options.static_mesh_import_data.set_editor_property("generate_lightmap_u_vs", True)
    options.static_mesh_import_data.set_editor_property("auto_generate_collision", True)
    return options


def build_skeletal_mesh_import_options(materials=True, textures=True):
    """
    导入skeletal
    :param materials: <bool> 是否导入材质球
    :param textures: <bool> 是否导入贴图
    :return:
    """
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_textures", textures)
    options.set_editor_property("import_materials", materials)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    options.set_editor_property("automated_import_should_detect_type", False)
    # unreal.FbxMeshImportData
    options.skeletal_mesh_import_data.set_editor_property("import_translation", unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property("import_rotation", unreal.Rotator(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property("import_uniform_scale", 1.0)
    # unreal.FbxSkeletalMeshImportData
    options.skeletal_mesh_import_data.set_editor_property("import_morph_targets", True)
    options.skeletal_mesh_import_data.set_editor_property("update_skeleton_reference_pose", False)
    return options


def build_fbx_import_options(as_skeletal=False, materials=True, textures=True):
    """
    导入fbx
    :param materials: <bool> 是否导入材质球
    :param textures: <bool> 是否导入贴图
    :param as_skeletal: 是否导入成骨架
    :return:
    """
    if as_skeletal:
        return build_skeletal_mesh_import_options(materials, textures)
    else:
        return build_static_mesh_import_options(materials, textures)


def build_animation_import_options(skeleton_path):
    """
    导入动画数据
    :param skeleton_path: content下skeleton mesh路径
    :return:
    """
    options = unreal.FbxImportUI()
    options.set_editor_property("import_animations", True)
    options.skeleton = unreal.load_asset(skeleton_path)
    # unreal.FbxMeshImportData
    options.anim_sequence_import_data.set_editor_property("import_translation", unreal.Vector(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property("import_rotation", unreal.Rotator(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property("import_uniform_scale", 1.0)
    # unreal.FbxAnimSequenceImportData
    # options.anim_sequence_import_data.set_editor_property("convert_scene", True)
    options.anim_sequence_import_data.set_editor_property("animation_length", unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    options.anim_sequence_import_data.set_editor_property("remove_redundant_keys", False)
    return options


def execute_import_tasks(tasks):
    """
    执行导入asset task
    :param tasks: <list>
    :return:
    """
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    imported_objects = list()
    for task in tasks:
        paths = task.get_editor_property("imported_object_paths")
        for path in paths:
            print "Imported: %s" % path
            imported_objects.append(path)
    return imported_objects


if __name__ == "_main__":
    TEXTURE_PATH = "D:/exr.png"
    FBX_PATH = "D:/duandao.fbx"
    SKELETON_PATH = "D:/resource/skeleton/GuLang_skin_skeleton.fbx"
    ANIMATION_PATH = "D:/resource/skeleton/GuLang_anim.fbx"
    # #################################################################################
    # ########################## import texture #######################################
    # #################################################################################
    texture_task = build_import_task(TEXTURE_PATH, "/Game/StarterContent/Textures")
    execute_import_tasks([texture_task])

    # #################################################################################
    # ########################## import static mesh ###################################
    # #################################################################################
    options = build_static_mesh_import_options()
    fbx_task = build_import_task(FBX_PATH, "/Game/MyGeometry", options)
    execute_import_tasks([fbx_task])

    # #################################################################################
    # ########################## import skeleton mesh #################################
    # #################################################################################
    options = build_skeletal_mesh_import_options()
    skeleton_task = build_import_task(SKELETON_PATH, "/Game/SkeletonMeshes", options)
    execute_import_tasks([skeleton_task])

    # #################################################################################
    # ########################## import animation #####################################
    # #################################################################################
    options = build_animation_import_options("/Game/SkeletonMeshes/GuLang_skin_skeleton_Skeleton")
    animation_task = build_import_task(ANIMATION_PATH, "/Game/Animations", options)
    execute_import_tasks([animation_task])
