import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .folders import *

class MyProperties(bpy.types.PropertyGroup):
    
    root_folder: bpy.props.EnumProperty(name="Root", description="Select a root", items=get_root_folders,) # type: ignore
    group_folder: bpy.props.EnumProperty(name="Group", description="Select a group", items=get_group_folders,) # type: ignore
    asset_folder: bpy.props.EnumProperty(name="Asset", description="Select an asset", items=get_asset_folders,) # type: ignore
    type_folder: bpy.props.EnumProperty(name="Type", description="Select a type", items=get_type_folders,) # type: ignore

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