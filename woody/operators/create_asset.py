from ..preferences import get_directory, get_blender_version
from ..lib.blender.save_current_scene import *
from ..lib.blender.new_blend import *
from ..lib.json.load_save_json_data import save_structure_to_json, load_json_data
from ..lib.json import *
from ..lib.folders.create_folders_subfolders import create_folders_subfolders

import bpy
from pathlib import Path

class PIPE_OT_create_asset(bpy.types.Operator):
    bl_idname = "pipe.create_asset"
    bl_label = "Create Asset"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        save_current_scene()

        base_path = Path(bpy.path.abspath(directory)) 
        save_structure_to_json(base_path) 

        data = load_json_data(context)
        if "assets" in data:
            scene.woody.root_folder = "assets" 
            groups = get_group_folders(self, context)
            if groups and groups[0][0] != "NONE":
                scene.woody.group_folder = groups[0][0] 

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()
        blenderVersion = get_blender_version()

        base_path = Path(bpy.path.abspath(directory))
        base_path = Path(base_path) / "assets" / my_props.group_folder

        folders = {
                my_props.asset: ["ref", "model", "lookdev", "rigging", "cg"],
        }

        create_folders_subfolders(folders, base_path)

        collection_name = f"assets_{my_props.group_folder}_{my_props.asset}_{my_props.typeAsset}"

        base_path = Path(base_path) / my_props.asset / my_props.typeAsset
        file_name = f"{my_props.asset}_{my_props.typeAsset}_latest.blend"
        full_path = base_path / file_name
        # ??? Why is there a keyword argument to parse the arguments ???
        new_blend(blender_exe=blenderVersion, new_file_name=full_path, collection_name=collection_name, config_path=None)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        my_props = context.scene.woody

        layout.prop(my_props, "group_folder")
        layout.prop(my_props, "asset")
        layout.prop(my_props, "typeAsset")