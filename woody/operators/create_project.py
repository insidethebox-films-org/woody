from ..lib.blender.get_preferences import get_directory
from ..lib.json import *
from ..lib.folders.create_folders_subfolders import create_folders_subfolders

import bpy
from pathlib import Path


class PIPE_OT_create_project(bpy.types.Operator):
    # Creates a new project with the correct folder structure in the base project directory

    bl_idname = "pipe.create_project"
    bl_label = "Create a new project"

    def execute(self, context):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        base_path = Path(bpy.path.abspath(directory))

        # Dictionary of folders and subfolders
        folders = {
                "assets": [],
                "shots": [],
                "_publish": [],
        }

        create_folders_subfolders(folders, base_path)
        create_default_proj_config(base_path)

        return {"FINISHED"}