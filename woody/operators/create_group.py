from ..lib.blender.get_preferences import get_directory
from ..lib.json.load_save_json_data import save_structure_to_json
from ..lib.folders.create_folders_subfolders import create_folders_subfolders

import bpy
from pathlib import Path

class PIPE_OT_create_group(bpy.types.Operator):
    bl_idname = "pipe.create_group"
    bl_label = "Create Group"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        base_path = Path(bpy.path.abspath(directory)) 
        save_structure_to_json(base_path)

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        base_path = Path(bpy.path.abspath(directory))
        base_path = Path(base_path) / my_props.root_folder

        # Dictionary of folders and subfolders
        if my_props.root_folder == "assets":
            folders = {
                my_props.group:{
                    "base": ["ref", "model", "lookdev", "rigging"]
                }

            }
        else:
            folders = {
                my_props.group:{
                    "base": ["ref", "layout", "FX", "lighting", "animation"]
                }

            }

        create_folders_subfolders(folders, base_path)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        my_props = context.scene.woody

        layout.prop(my_props, "root_folder")
        layout.prop(my_props, "group")