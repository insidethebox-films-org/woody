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
        create_default_proj_config(base_path)

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

# ??? Operator is called Open asset but also opens shots ???
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
        config_path = Path(bpy.path.abspath(directory)) / my_props.root_folder / my_props.group_folder / my_props.asset_folder / "shot_config.json"
        file_name = f"{my_props.asset_folder}_{my_props.type_folder}_latest.blend"
        full_path = base_path / file_name
        open_blend(blender_exe=blenderVersion, blend_file_path=full_path, config_path=config_path)

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
        export_filename = asset + "_" + type_ + "_published" + ".blend"
        export_path = filePath / export_filename

        print("EXPRTPATH: ", export_path)
        create_blend_with_collection(export_filename, collection_name, filePath)

        # Feedback (status bar + popup)
        self.report({'INFO'}, f"✅ Published to: {export_filename}")
        show_popup_message("✅ Asset has been published!", title="Publish Complete", icon='CHECKMARK')
        
        return {"FINISHED"}

class PIPE_OT_set_output_cg(bpy.types.Operator):
    bl_idname = "pipe.set_output_cg"
    bl_label = "Set Output to CG Folder"
    bl_description = "Set render output path to the cg folder"

    def execute(self, context):
        print("GET DIR: ",get_directory())
        success = set_render_output_to_cg()
        if success:
            self.report({'INFO'}, "✅ Render output path set to CG folder")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "⚠️ Could not set path — are you in a valid asset/shot file?")
            return {'CANCELLED'}

class PIPE_OT_apply_render_config(bpy.types.Operator):
    bl_idname = "pipe.apply_render_config"
    bl_label = "Apply Render Config"
    bl_description = "Apply settings from projConfig.json"

    def execute(self, context):
        blend_path = bpy.data.filepath
        if not blend_path:
            self.report({'WARNING'}, "⚠️ Could not set path — are you in a valid asset/shot file?")
            return {'CANCELLED'}
        
        project_root = get_directory()

        if not project_root:
            self.report({'WARNING'}, "⚠️ Could not find project root")
            return {'CANCELLED'}

        config_path = os.path.join(project_root, "projConfig.json")
        if not os.path.isfile(config_path):
            self.report({'WARNING'}, f"⚠️ No projConfig.json found at: {config_path}")
            return {'CANCELLED'}

        apply_render_config(config_path)
        self.report({'INFO'}, f"✅ Render config applied from {config_path}")
        return {'FINISHED'}
    
class PIPE_OT_render_with_prompt(bpy.types.Operator):
    bl_idname = "pipe.render_with_prompt"
    bl_label = "Render"
    bl_description = "Render animation with version check"

    choice: bpy.props.EnumProperty(
        name="Render Option",
        items=[
            ('OVERWRITE', "Overwrite", "Overwrite existing files"),
            ('NEW_VERSION', "New Version", "Create a new version and render there"),
        ],
        default='OVERWRITE'
    )  # type: ignore

    def execute(self, context):
        render_path = Path(bpy.path.abspath(context.scene.render.filepath))

        # Check that we're in a valid asset/shot path
        if not bpy.data.filepath:
            self.report({'ERROR'}, "🚨 File not saved yet.")
            return {'CANCELLED'}

        root, group, asset, type_ = context_names()
        if root not in {"assets", "shots"} or group == "GROUP" or asset == "ASSET":
            self.report({'ERROR'}, f"🚨 Unexpected path: {root}/{group}/{asset}")
            return {'CANCELLED'}

        if self.choice == 'NEW_VERSION':
            success = set_render_output_to_cg()
            if not success:
                self.report({'ERROR'}, "⚠️ Failed to set a new version render path.")
                return {'CANCELLED'}

            render_path = Path(bpy.path.abspath(context.scene.render.filepath))
            self.report({'INFO'}, f"🆕 New version folder set: {render_path}")

        else:
            self.report({'INFO'}, f"📝 Overwriting frames in: {render_path}")
        
        bpy.ops.wm.save_mainfile()
        bpy.ops.render.render(animation=True)
        return {'FINISHED'}

    def invoke(self, context, event):
        render_path = Path(bpy.path.abspath(context.scene.render.filepath))

        # Check that we're in a valid asset/shot path
        if not bpy.data.filepath:
            self.report({'ERROR'}, "🚨 File not saved yet.")
            return {'CANCELLED'}

        root, group, asset, type_ = context_names()
        if root not in {"assets", "shots"} or group == "GROUP" or asset == "ASSET":
            self.report({'ERROR'}, f"🚨 Unexpected path: {root}/{group}/{asset}")
            return {'CANCELLED'}

        if not render_path.is_dir():
            return self.execute(context)

        has_existing_frames = any(
            f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.exr', '.blend')
            for f in render_path.iterdir()
            if f.is_file()
        )

        if has_existing_frames:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Output folder has existing frames.")
        layout.prop(self, "choice", expand=True)

class PIPE_OT_set_frame_range(bpy.types.Operator):
    bl_idname = "pipe.set_frame_range"
    bl_label = "Set Frame Range"
    bl_description = "Update scene frame range and shot config file"

    frame_start: bpy.props.IntProperty(name="Start Frame")# type:ignore
    frame_end: bpy.props.IntProperty(name="End Frame")# type:ignore

    def execute(self, context):
        scene = context.scene
        root, group, asset, type_ = context_names()

        if root=="shots":
            config_path = Path(bpy.path.abspath("//")).parent / "shot_config.json"

            data = {}
            if config_path.exists():
                with open(config_path, "r") as f:
                    data = json.load(f)

            # Update with UI values
            data["frame_start"] = scene.shot_frame_start
            data["frame_end"] = scene.shot_frame_end

            with open(config_path, "w") as f:
                json.dump(data, f, indent=4)

        # Apply to scene
        scene.frame_start = scene.shot_frame_start
        scene.frame_end = scene.shot_frame_end

        self.report({'INFO'}, "Frame range updated")
        return {'FINISHED'}

# Woody Asset Browser

class PIPE_OT_open_publish(bpy.types.Operator):
    bl_idname = "pipe.open_publish"
    bl_label = "Open Publish"
    bl_description = "Link the first collection from a published .blend file into the current scene"

    filepath: bpy.props.StringProperty()# type:ignore

    def execute(self, context):
        blend_path = Path(self.filepath).resolve()
        current_path = Path(bpy.data.filepath).resolve()

        # Extract root/group/asset from both paths
        try:
            def extract_asset_path_parts(path):
                path = Path(path)
                filename = path.stem  # e.g. "lupinPub_model_published"
                
                # Assuming the format is always: asset_type_status
                filename_parts = filename.split("_")
                if len(filename_parts) < 3:
                    raise ValueError(f"Unexpected filename format: {filename}")
                
                asset = filename_parts[0]
                type_ = filename_parts[1]
                
                parts = path.parts
                if len(parts) < 5:
                    return None
                group = parts[-4]
                root = parts[-5]
                
                return root, group, asset, type_

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

          # Determine expected collection name
        root, group, asset, type_ = extract_asset_path_parts(blend_path)
        target_collection_name = f"{root}_{group}_{asset}_{type_}"
        print("BLEND PATH: ",blend_path)
        print("TARGET: ",target_collection_name)
        try:
            with bpy.data.libraries.load(str(blend_path), link=True) as (data_from, data_to):
                if target_collection_name not in data_from.collections:
                    self.report({'ERROR'}, f"Expected collection '{target_collection_name}' not found in .blend")
                    return {'CANCELLED'}

                data_to.collections = [target_collection_name]


            linked_col = data_to.collections[0]
            context.scene.collection.children.link(linked_col)

            self.report({'INFO'}, f"✅ Linked collection: {linked_col.name}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Linking failed: {e}")
            return {'CANCELLED'}

class PIPE_OT_clear_enum(bpy.types.Operator):
    bl_idname = "pipe.clear_enum"
    bl_label = "Clear Selection"
    bl_description = "Reset this field to 'None'"

    prop_name: bpy.props.StringProperty()# type:ignore

    def execute(self, context):
        setattr(context.scene.woody, self.prop_name, "NONE")
        return {'FINISHED'}

class PIPE_OT_override_collection(bpy.types.Operator):
    bl_idname = "pipe.override_collection"
    bl_label = "Override Linked Collection"
    bl_description = "Create a full library override (content) for the specified linked collection"

    collection_name: bpy.props.StringProperty()# type:ignore

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
        