from ..lib.blender.get_preferences import get_directory, get_blender_version
from ..lib.blender.save_current_scene import *
from ..lib.blender.new_blend import *
from ..lib.json.load_save_json_data import save_structure_to_json, load_json_data
from ..lib.json import *
from ..lib.folders.create_folders_subfolders import create_folders_subfolders

import bpy
from pathlib import Path

class PIPE_OT_create_shot(bpy.types.Operator):
    bl_idname = "pipe.create_shot"
    bl_label = "Create Shot"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        save_current_scene()

        base_path = Path(bpy.path.abspath(directory)) 
        save_structure_to_json(base_path)  

        data = load_json_data(context)
        if "shots" in data:
            scene.woody.root_folder = "shots" 
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
        base_path = Path(base_path) / "shots" / my_props.group_folder

        # Dictionary of folders and subfolders
        folders = {
                my_props.shot: ["ref", "layout", "FX", "lighting", "animation", "cg"],
        }

        create_folders_subfolders(folders, base_path)
        
        config_path = base_path / my_props.shot / "shot_config.json"
        config_data = {
            "frame_start": 0,
            "frame_end": 100,
        }
        create_shot_config_file(config_path, config_data)

        collection_name = f"shots_{my_props.group_folder}_{my_props.shot}_{my_props.typeShot}"

        base_path = Path(base_path) / my_props.shot / my_props.typeShot
        file_name = f"{my_props.shot}_{my_props.typeShot}_latest.blend"
        full_path = base_path / file_name
        new_blend(blender_exe=blenderVersion, new_file_name=full_path, collection_name=collection_name, config_path=config_path)

        return {"FINISHED"}


    def draw(self, context):
        layout = self.layout
        my_props = context.scene.woody

        layout.prop(my_props, "group_folder")
        layout.prop(my_props, "shot")
        layout.prop(my_props, "typeShot")