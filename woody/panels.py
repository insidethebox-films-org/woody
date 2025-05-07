import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .context import *

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

        row1 = layout.row()
        row1.operator("pipe.publish_prep", text="Publish Prep", icon="SURFACE_NSPHERE")
        row1.operator("pipe.create_publish_workspace", text="Workspace", icon="WINDOW")

        layout.operator("pipe.publish_asset", text="Publish", icon="DISK_DRIVE")

        row2 = layout.row()
        row2.operator("pipe.fv_publish", text="FV_Publish2", icon="DISK_DRIVE")
        