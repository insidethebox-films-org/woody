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

class PIPE_OT_publish(bpy.types.Operator):
    bl_idname = "pipe.publish"
    bl_label = "Publish"
    bl_description = "Publish the current asset to a dedicated file"

    def invoke(self, context, event):
        # This opens a Blender-native confirmation popup
        return context.window_manager.invoke_confirm(self, event)
    
    def execute(self, context):

        directory = get_directory()
        directory = Path(directory)

        print("DIRECTORY:  ",directory)

        root, group, asset, type_ = context_names()
        collection_name = root + "_" + group + "_" + asset + "_" + type_
        tags = [root, group, asset, type_]

        collection = bpy.data.collections.get(collection_name)

        filePath = directory / root / group / asset / "_publish" 
        print("FILEPATH: ", filePath)

        #export_dir = directory / "_publish"
        export_filename = asset + "_published" + ".blend"
        export_path = filePath / export_filename

        print("EXPRTPATH: ", export_path)
        create_blend_with_collection(export_filename, collection_name, filePath)

        # Feedback (status bar + popup)
        self.report({'INFO'}, f"✅ Published to: {export_filename}")
        show_popup_message("✅ Asset has been published!", title="Publish Complete", icon='CHECKMARK')
        
        return {"FINISHED"}

from pathlib import Path

class PIPE_OT_open_publish(bpy.types.Operator):
    bl_idname = "pipe.open_publish"
    bl_label = "Open Publish"
    bl_description = "Link the first collection from a published .blend file into the current scene"

    filepath: bpy.props.StringProperty()

    def execute(self, context):
        blend_path = Path(self.filepath).resolve()
        current_path = Path(bpy.data.filepath).resolve()

        # Extract root/group/asset from both paths
        try:
            def extract_asset_path_parts(path):
                # Example: /project/assets/Root/Group/Asset/_publish/asset_published.blend
                parts = path.parts
                if len(parts) < 5:
                    return None
                # Grab asset, group, root in reverse order
                asset = parts[-3]
                group = parts[-4]
                root = parts[-5]
                return (root, group, asset)

            current_parts = extract_asset_path_parts(current_path)
            target_parts = extract_asset_path_parts(blend_path)

            if current_parts and target_parts and current_parts == target_parts:
                self.report({'ERROR'}, "❌ Cannot link from the same asset you're currently working in.")
                return {'CANCELLED'}

        except Exception as e:
            self.report({'WARNING'}, f"⚠️ Asset path check failed: {e}")
            # Allow linking if check fails

        if not blend_path.exists():
            self.report({'ERROR'}, f"File not found: {blend_path}")
            return {'CANCELLED'}

        try:
            with bpy.data.libraries.load(str(blend_path), link=True) as (data_from, data_to):
                if not data_from.collections:
                    self.report({'ERROR'}, "No collections found in this .blend file.")
                    return {'CANCELLED'}

                collection_name = data_from.collections[0]
                data_to.collections = [collection_name]

            linked_col = data_to.collections[0]
            context.scene.collection.children.link(linked_col)

            self.report({'INFO'}, f"✅ Linked collection: {collection_name}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Linking failed: {e}")
            return {'CANCELLED'}

class PIPE_OT_clear_enum(bpy.types.Operator):
    bl_idname = "pipe.clear_enum"
    bl_label = "Clear Selection"
    bl_description = "Reset this field to 'None'"

    prop_name: bpy.props.StringProperty()

    def execute(self, context):
        setattr(context.scene.woody, self.prop_name, "NONE")
        return {'FINISHED'}

class PIPE_OT_override_collection(bpy.types.Operator):
    bl_idname = "pipe.override_collection"
    bl_label = "Override Linked Collection"
    bl_description = "Create a full library override (content) for the specified linked collection"

    collection_name: bpy.props.StringProperty()

    def execute(self, context):
        col = bpy.data.collections.get(self.collection_name)
        if not col:
            self.report({'ERROR'}, f"Collection '{self.collection_name}' not found.")
            return {'CANCELLED'}

        if col.override_library:
            self.report({'INFO'}, f"Collection '{col.name}' is already overridden.")
            return {'CANCELLED'}

        try:
            override = col.override_hierarchy_create(
                scene=context.scene,
                view_layer=context.view_layer,
                do_fully_editable=True
            )

            # Attempt to unlink original linked collection from scene
            children = context.scene.collection.children
            for child in children:
                if child.name == col.name:
                    children.unlink(child)
                    self.report({'INFO'}, f"Unlinked original linked collection: {child.name}")
                    break

            self.report({'INFO'}, f"Full override created for: {override.name}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Override failed: {e}")
            return {'CANCELLED'}
        