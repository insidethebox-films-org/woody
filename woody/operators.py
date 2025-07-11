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

class PIPE_OT_publish_prep(bpy.types.Operator): # DEPRECATED
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

class PIPE_OT_create_publish_workspace(bpy.types.Operator):  # DEPRECATED
    bl_idname = "pipe.create_publish_workspace"
    bl_label = "Publish Asset"

    def execute(self, context):

        create_publish_workspace("Layout")
        rename_workspace("Layout", "Publish")

        return {"FINISHED"}

class PIPE_OT_publish(bpy.types.Operator):  # DEPRECATED

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
        create_blend_with_collection_FV(export_filename, collection_name, filePath)

        return {"FINISHED"}

def get_blend_items(self, context):
    base_dir = get_directory()
    items = []

    if not base_dir:
        return [("NONE", "No directory", "")]

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith("_published.blend"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                # Unique identifier, label, tooltip
                items.append((full_path, rel_path, "Link this file"))

    if not items:
        return [("NONE", "No published files found", "")]
    return items

def find_layer_collection(layer_collection, target_collection):
    """Recursively search for a LayerCollection matching the target collection"""
    if layer_collection.collection == target_collection:
        return layer_collection
    for child in layer_collection.children:
        result = find_layer_collection(child, target_collection)
        if result:
            return result
    return None
class PIPE_FVopenPublish(bpy.types.Operator):
    bl_idname = "pipe.fv_openpublish"
    bl_label = "FV Open Publish"
    bl_description = "Link the first collection from a published .blend file into the current scene"

    filepath: bpy.props.StringProperty()

    def execute(self, context):
        blend_path = self.filepath

        if not Path(blend_path).exists():
            self.report({'ERROR'}, f"File not found: {blend_path}")
            return {'CANCELLED'}

        try:
            with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
                if not data_from.collections:
                    self.report({'ERROR'}, "No collections found in this .blend file.")
                    return {'CANCELLED'}

                # Link the first collection
                collection_name = data_from.collections[0]
                data_to.collections = [collection_name]

            linked_col = data_to.collections[0]
            context.scene.collection.children.link(linked_col)

            self.report({'INFO'}, f"✅ Linked collection: {collection_name}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Linking failed: {e}")
            return {'CANCELLED'}

class PIPE_FVClearEnum(bpy.types.Operator):
    bl_idname = "pipe.clear_enum"
    bl_label = "Clear Selection"
    bl_description = "Reset this field to 'None'"

    prop_name: bpy.props.StringProperty()

    def execute(self, context):
        setattr(context.scene.woody, self.prop_name, "NONE")
        return {'FINISHED'}

#LATEST GOOD 
# class PIPE_FVoverride_collection(bpy.types.Operator):
#     bl_idname = "pipe.override_collection"
#     bl_label = "Override Linked Collection"
#     bl_description = "Make a library override for this linked collection"

#     collection_name: bpy.props.StringProperty()

#     def execute(self, context):
#         collection = bpy.data.collections.get(self.collection_name)
#         if not collection:
#             self.report({'ERROR'}, f"Collection '{self.collection_name}' not found.")
#             return {'CANCELLED'}

#         # Find the Outliner area and override the context
#         for area in context.window.screen.areas:
#             if area.type == 'OUTLINER':
#                 for region in area.regions:
#                     if region.type == 'WINDOW':
#                         override = {
#                             'window': context.window,
#                             'screen': context.screen,
#                             'area': area,
#                             'region': region,
#                             'scene': context.scene,
#                             'id': collection,
#                             'space_data': area.spaces.active,
#                         }

#                         try:
#                             bpy.ops.outliner.collection_library_override_create(override)
#                             self.report({'INFO'}, f"Overridden: {collection.name}")
#                             return {'FINISHED'}
#                         except Exception as e:
#                             self.report({'ERROR'}, f"Override failed: {e}")
#                             return {'CANCELLED'}

#         self.report({'ERROR'}, "No Outliner area found.")
#         return {'CANCELLED'}


# class PIPE_FVoverride_collection(bpy.types.Operator):
#     bl_idname = "pipe.override_collection"
#     bl_label = "Override Linked Collection"
#     bl_description = "Create a full library override (content) for the specified linked collection"

#     collection_name: bpy.props.StringProperty()

#     def execute(self, context):
#         collection = bpy.data.collections.get(self.collection_name)
#         if not collection:
#             self.report({'ERROR'}, f"Collection '{self.collection_name}' not found.")
#             return {'CANCELLED'}

#         # Check if it's already overridden
#         if collection.override_library:
#             self.report({'INFO'}, f"Collection '{collection.name}' is already overridden.")
#             return {'CANCELLED'}

#         # Prepare the root object to override (we need an instance in the scene)
#         for obj in context.scene.objects:
#             if obj.instance_type == 'COLLECTION' and obj.instance_collection == collection:
#                 try:
#                     override = bpy.data.override_library_create(
#                         reference=obj,
#                         context=context,
#                         library=bpy.data.libraries[collection.library.name],
#                         do_hierarchy=True
#                     )
#                     self.report({'INFO'}, f"Created override: {override.name}")
#                     return {'FINISHED'}
#                 except Exception as e:
#                     self.report({'ERROR'}, f"Override failed: {e}")
#                     return {'CANCELLED'}

#         # No existing instance object found, so create one
#         try:
#             instance_obj = bpy.data.objects.new(name=f"{collection.name}_instance", object_data=None)
#             instance_obj.instance_type = 'COLLECTION'
#             instance_obj.instance_collection = collection
#             context.scene.collection.objects.link(instance_obj)

#             override = bpy.data.override_library_create(
#                 reference=instance_obj,
#                 context=context,
#                 library=bpy.data.libraries[collection.library.name],
#                 do_hierarchy=True
#             )
#             self.report({'INFO'}, f"Instancer created and overridden: {override.name}")
#             return {'FINISHED'}
#         except Exception as e:
#             self.report({'ERROR'}, f"Failed to create override: {e}")
#             return {'CANCELLED'}

class PIPE_FVoverride_collection(bpy.types.Operator):
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


        
# class PIPE_FVoverride_collection(bpy.types.Operator):
#     bl_idname = "pipe.override_collection"
#     bl_label = "Override Linked Collection"
#     bl_description = "Make a library override for this linked collection"

#     collection_name: bpy.props.StringProperty()

#     def execute(self, context):
#         collection = bpy.data.collections.get(self.collection_name)
#         if not collection:
#             self.report({'ERROR'}, f"Collection '{self.collection_name}' not found.")
#             return {'CANCELLED'}

#         # Find an object instancing this collection
#         for obj in bpy.data.objects:
#             if obj.instance_type == 'COLLECTION' and obj.instance_collection == collection:
#                 # Select and activate this object
#                 bpy.ops.object.select_all(action='DESELECT')
#                 obj.select_set(True)
#                 context.view_layer.objects.active = obj

#                 # Perform the override
#                 bpy.ops.object.make_override_library()
#                 self.report({'INFO'}, f"Overridden: {collection.name}")
#                 return {'FINISHED'}

#         self.report({'WARNING'}, f"No instancing object found for '{collection.name}'")
#         return {'CANCELLED'}
    