import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .utils import *
from .folders import *
from .blend_functions import *
from .context import *
from .catalogs import *

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

        return {"FINISHED"}
    
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
                my_props.asset: ["ref", "model", "lookdev", "rigging"],
        }

        create_folders_subfolders(folders, base_path)

        base_path = Path(base_path) / my_props.asset / my_props.typeAsset
        file_name = f"{my_props.asset}_{my_props.typeAsset}_latest.blend"
        full_path = base_path / file_name
        new_blend(blender_exe=blenderVersion, new_file_name=full_path)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        my_props = context.scene.woody

        layout.prop(my_props, "group_folder")
        layout.prop(my_props, "asset")
        layout.prop(my_props, "typeAsset")

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
                my_props.shot: ["ref", "layout", "FX", "lighting", "animation"],
        }

        create_folders_subfolders(folders, base_path)

        base_path = Path(base_path) / my_props.shot / my_props.typeShot
        file_name = f"{my_props.shot}_{my_props.typeShot}_latest.blend"
        full_path = base_path / file_name
        new_blend(blender_exe=blenderVersion, new_file_name=full_path)

        return {"FINISHED"}


    def draw(self, context):
        layout = self.layout
        my_props = context.scene.woody

        layout.prop(my_props, "group_folder")
        layout.prop(my_props, "shot")
        layout.prop(my_props, "typeShot")

class PIPE_OT_open_asset(bpy.types.Operator):

    bl_idname = "pipe.open_asset"
    bl_label = "Open Asset"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        save_current_scene()

        base_path = Path(bpy.path.abspath(directory))
        save_structure_to_json(base_path)  # Save the JSON before showing the popup

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()
        blenderVersion = get_blender_version()

        base_path = Path(bpy.path.abspath(directory)) / my_props.root_folder / my_props.group_folder / my_props.asset_folder / my_props.type_folder
        file_name = f"{my_props.asset_folder}_{my_props.type_folder}_latest.blend"
        full_path = base_path / file_name
        open_blend(blender_exe=blenderVersion, blend_file_path=full_path)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        my_props = context.scene.woody

        layout.prop(my_props, "root_folder")
        layout.prop(my_props, "group_folder")
        layout.prop(my_props, "asset_folder")
        layout.prop(my_props, "type_folder")

class PIPE_OT_version_up(bpy.types.Operator):

    bl_idname = "pipe.save_asset"
    bl_label = "Save Asset"

    def execute(self, context):

        save_current_scene()

        current_path = Path(bpy.data.filepath)
        filename = current_path.stem
        print(filename)
        filename = filename.replace("_latest" , "")

        incremental_save(new_name=filename)

        return {"FINISHED"}

class PIPE_OT_publish_prep(bpy.types.Operator):
    bl_idname = "pipe.publish_prep"
    bl_label = "Publish Asset"

    def execute(self, context):
        
        directory = get_directory()
        directory = Path(directory)

        root, group, asset, type_ = context_names()
        collection_name = root + "_" + group + "_" + asset + "_" + type_
        tags = [root, group, asset, type_]

        file_path = Path(directory) / "_publish" / "blender_assets.cats.txt"
        add_to_catalog_file(collection_name, file_path)

        publish(collection_name, tags)

        export_dir = directory / "_publish" / "blends"
        export_filename = collection_name + ".blend"
        export_path = export_dir / export_filename

        create_blend_with_collection(export_filename, collection_name, export_dir)
        
        open_publish_blend_file(export_path)

        select_objects_in_selected_collection(collection_name)

        export_geo_dir = directory / "_publish" / "geo" / collection_name
        export_file = collection_name + ".usdc"
        export_geo_path = export_geo_dir / export_file

        export_selection_to_usd(str(export_geo_path), export_format="USDC")

        save_current_scene()

        restart_blend_file()

        return {"FINISHED"}

class PIPE_OT_create_publish_workspace(bpy.types.Operator):
    bl_idname = "pipe.create_publish_workspace"
    bl_label = "Publish Asset"

    def execute(self, context):

        create_publish_workspace("Layout")
        rename_workspace("Layout", "Publish")

        return {"FINISHED"}

class PIPE_OT_publish(bpy.types.Operator):

    bl_idname = "pipe.publish_asset"
    bl_label = "Publish Asset"

    def execute(self, context):

        directory = get_directory()
        directory = Path(directory)

        file_path = bpy.data.filepath
        file_name = os.path.basename(file_path)
        file_name = file_name.replace(".blend", "")

        collection_name = file_name
        
        import_geo_dir = directory / "_publish" / "geo" / collection_name
        import_file = collection_name + ".usdc"
        import_geo_path = os.path.join(import_geo_dir, import_file)

        delete_collection_contents(collection_name)
        import_usdc_to_collection(import_geo_path, collection_name)

        return {"FINISHED"}

class PIPE_FVpublish(bpy.types.Operator):
    bl_idname = "pipe.fv_publish"
    bl_label = "FV Publish"
    def execute(self, context):
        return {"FINISHED"}

