import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .context import *
from .preferences import *

class VIEW3D_PT_context(bpy.types.Panel):
     
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Context"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout

        root, group, asset, type_ = context_names()
         
        rootBox = layout.box()
        rootBox.label(text=f"root - {root}", icon="OUTLINER")
        rootBox.scale_y = 0.75

        groupBox = layout.box()
        groupBox.label(text=f"group - {group}", icon="GROUP_VERTEX")
        groupBox.scale_y = 0.75

        assetBox = layout.box()
        assetBox.label(text=f"asset - {asset}", icon="MESH_CUBE")
        assetBox.scale_y = 0.75

        typeBox = layout.box()
        typeBox.label(text=f"type - {type_}", icon="OUTLINER_DATA_POINTCLOUD")
        typeBox.scale_y = 0.75

# Asset

class VIEW3D_PT_assets_shots(bpy.types.Panel):
     
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Assets/Shots"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout

        newAssetBox = layout.box()
        newAssetBox.label(text="New")
        newAssetBox.scale_y = 0.65

        layout.operator("pipe.create_group", text="New Group", icon="GROUP_VERTEX")

        row1 = self.layout.row()
        row1.operator("pipe.create_asset", text="New Asset", icon="OUTLINER_OB_META")
        row1.operator("pipe.create_shot", text="New Shot", icon="VIEW_CAMERA")

        fileBox = layout.box()
        fileBox.label(text="File")
        fileBox.scale_y = 0.65

        row2 = self.layout.row()
        row2.operator("pipe.open_asset", text="Open", icon="COPY_ID")
        row2.operator("pipe.save_asset", text="Save", icon="NODE_COMPOSITING")
        
        publishBox = layout.box()
        publishBox.label(text="Publish")
        publishBox.scale_y = 0.65
        
        row3 = layout.row()
        row3.operator("pipe.publish", text="Publish", icon="DISK_DRIVE")
        
        publishBox = layout.box()
        publishBox.label(text="Render")
        publishBox.scale_y = 0.65

        row4 = layout.row()
        row4.operator("pipe.set_output_cg", text="Set Render Path", icon="RENDER_STILL")
        row4.operator("pipe.apply_render_config", text="Set Configs", icon="PREFERENCES")
        
        layout.operator("pipe.render_with_prompt", text="Render", icon="RENDER_ANIMATION")

# Publish Asset Browser

def is_collection_linked_and_not_overridden(col):
    if not col.library:
        return False
    if col.name not in [c.name for c in bpy.context.scene.collection.children]:
        return False
    for other in bpy.data.collections:
        if other.override_library and other.override_library.reference == col:
            return False
    return "_published.blend" in col.library.filepath

def is_collection_override_of_published(col):
    if not col.override_library:
        return False

    # Make sure it's directly in the scene
    if col.name not in [c.name for c in bpy.context.scene.collection.children]:
        return False

    ref = col.override_library.reference
    if not ref or not ref.library:
        return False

    return "_published.blend" in ref.library.filepath

def is_published_file_already_in_scene(blend_path):
    for c in bpy.data.collections:
        if c.library and c.library.filepath == blend_path and not c.override_library:
            if c.name in [cc.name for cc in bpy.context.scene.collection.children]:
                return True
        if c.override_library:
            ref = c.override_library.reference
            if ref and ref.library and ref.library.filepath == blend_path:
                if c.name in [cc.name for cc in bpy.context.scene.collection.children]:
                    return True
    return False

class VIEW3D_PT_publish_browser(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Woody Asset Browser"
    bl_category = "WoodyAssetBrowser"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.woody

        def draw_enum_with_clear(layout, prop_id, label=""):
            row = layout.row(align=True)
            row.prop(props, prop_id, text=label)
            op = row.operator("pipe.clear_enum", text="", icon="X")
            op.prop_name = prop_id

        draw_enum_with_clear(layout, "root_folder", "Root")
        draw_enum_with_clear(layout, "group_folder", "Group")
        draw_enum_with_clear(layout, "asset_folder", "Asset")

        layout.separator()
        layout.label(text="Published Files:")

        box = layout.box()
        col = box.column()
        col.scale_y = 0.95

        base_path = Path(bpy.path.abspath(get_directory()))
        if props.root_folder and props.root_folder != "NONE":
            base_path /= props.root_folder
            if props.group_folder and props.group_folder != "NONE":
                base_path /= props.group_folder
                if props.asset_folder and props.asset_folder != "NONE":
                    base_path /= props.asset_folder
        if not base_path.exists():
            layout.label(text="Invalid path.", icon="ERROR")
            return

        blend_files = list(base_path.rglob("*_published.blend"))

        if blend_files:
            for blend_file in blend_files:
                row = col.row(align=True)
                row.label(text=blend_file.name, icon="FILE_BLEND")

                # Get the relative blend path to match against linked/overridden collections
                blend_path_str = str(blend_file)

                # Check if already linked or overridden
                if not is_published_file_already_in_scene(blend_path_str):
                    op = row.operator("pipe.open_publish", text="", icon="IMPORT")
                    op.filepath = blend_path_str
                else:
                    row.label(icon="CHECKMARK")
        else:
            layout.label(text="No published files found.", icon="INFO")


        layout.separator()
        layout.label(text="Linked Published Collections:")
        box = layout.box()
        col = box.column()

        linked_collections = [
            c for c in bpy.data.collections if is_collection_linked_and_not_overridden(c)
        ]

        if linked_collections:
            for col_item in linked_collections:
                row = col.row(align=True)
                row.label(text=col_item.name, icon="OUTLINER_COLLECTION")
                op = row.operator("pipe.override_collection", text="", icon="IMPORT")
                op.collection_name = col_item.name
        else:
            col.label(text="No linked published collections.")

        layout.separator()
        layout.label(text="Overridden Published Collections:")
        box = layout.box()
        col = box.column()

        overridden_collections = [
            c for c in bpy.data.collections if is_collection_override_of_published(c)
        ]

        if overridden_collections:
            for col_item in overridden_collections:
                row = col.row(align=True)
                row.label(text=col_item.name, icon="LIBRARY_DATA_OVERRIDE")
        else:
            col.label(text="No overridden published collections.")
