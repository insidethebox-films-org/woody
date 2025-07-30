bl_info = {
    "name": "Woody",
    "author": "Oscar Bartle",
    "version": (0,2,1),     
    "blender": (4,2,5),
    "location": "3D Viewport > Sidebar > Woody",
    "description": "A pipeline tool",
    "category": "Development",
}

import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .properties import MyProperties
from .preferences import Preferences
from .operators import PIPE_OT_create_project, PIPE_OT_create_group, PIPE_OT_create_asset, PIPE_OT_create_shot, PIPE_OT_open_asset, PIPE_OT_version_up, PIPE_OT_publish, PIPE_OT_open_publish, PIPE_OT_clear_enum, PIPE_OT_override_collection, PIPE_OT_create_camera
from .panels import VIEW3D_PT_context, VIEW3D_PT_assets_shots, VIEW3D_PT_publish_browser, VIEW3D_PT_turntable

ADDON_NAME = __name__

#===============              
# Registration
#===============              
        
classes = [
    MyProperties,
    PIPE_OT_create_project,
    PIPE_OT_create_group,
    PIPE_OT_create_asset,
    PIPE_OT_create_shot,
    PIPE_OT_open_asset,
    PIPE_OT_version_up,
    PIPE_OT_publish,
    PIPE_OT_open_publish,
    PIPE_OT_clear_enum,
    PIPE_OT_override_collection,
    PIPE_OT_create_camera,
    Preferences,
    VIEW3D_PT_context,
    VIEW3D_PT_assets_shots,
    VIEW3D_PT_publish_browser,
    VIEW3D_PT_turntable,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        bpy.types.Scene.woody = bpy.props.PointerProperty(type= MyProperties)

def unregister():
    for cls in reversed(classes):  # reversed is safer for dependencies
        bpy.utils.unregister_class(cls)
    
    if hasattr(bpy.types.Scene, "woody"):
        del bpy.types.Scene.woody

if __name__ == "__main__":
    register()