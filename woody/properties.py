import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .folders import *

def update_root(self, context):
    self.group_folder = "NONE"
    self.asset_folder = "NONE"
    self.type_folder = "NONE"

def update_group(self, context):
    self.asset_folder = "NONE"
    self.type_folder = "NONE"

def update_asset(self, context):
    self.type_folder = "NONE"

class MyProperties(bpy.types.PropertyGroup):
    root_folder: bpy.props.EnumProperty(
        name="Root",
        description="Choose a root folder",
        items=get_root_folders,
        update=update_root
    )# type: ignore

    group_folder: bpy.props.EnumProperty(
        name="Group",
        description="Choose a group folder",
        items=get_group_folders,
        update=update_group
    )# type: ignore

    asset_folder: bpy.props.EnumProperty(
        name="Asset",
        description="Choose an asset folder",
        items=get_asset_folders,
        update=update_asset
    )# type: ignore

    type_folder: bpy.props.EnumProperty(
        name="Type",
        description="Choose a type folder",
        items=get_type_folders
    )# type: ignore

    group: bpy.props.StringProperty(name="Group", description="Name of new group") # type: ignore
    asset: bpy.props.StringProperty(name="Asset", description="Name of new asset") # type: ignore
    shot: bpy.props.StringProperty(name="Shot", description="Name of new shot") # type: ignore

    typeAsset: bpy.props.EnumProperty(
        name="Type",
        description="Choose an asset type",
        items=[
            ("ref", "ref", "ref"),
            ("model", "model", "model"),
            ("lookdev", "lookdev", "lookdev")
        ],
        default="model"  # Default value
    ) # type: ignore
    typeShot: bpy.props.EnumProperty(
        name="Shot",
        description="Choose an shot type",
        items=[
            ("layout", "layout", "layout"),
            ("animation", "animation", "animation"),
            ("FX", "FX", "FX"),
            ("lighting", "lighting", "lighting")
        ],
        default="layout"  # Default value
    ) # type: ignore