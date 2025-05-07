import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

ADDON_NAME = 'woody'

class Preferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME

    directory: bpy.props.StringProperty(name= "Directory", subtype='FILE_PATH', description="The directory of your project") # type: ignore
    blenderVersion: bpy.props.StringProperty(name= "EXE Path", subtype='FILE_PATH', description="Path to your blender.exe") # type: ignore

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_props = scene.woody
        
        pathsBox = layout.box()
        pathsBox.label(text="Paths")
        pathsBox.scale_y = 0.65

        layout.prop(self, "directory")
        layout.prop(self, "blenderVersion")

        projectBox = layout.box()
        projectBox.label(text="Project")
        projectBox.scale_y = 0.65

        row1 = self.layout.row()
        row1.operator("pipe.create_project", text="Create Project", icon="WORLD")
        row1.operator("wm.save_userpref", text="Save Project", icon="DOCUMENTS")

def get_preferences():
    preferences = bpy.context.preferences.addons[ADDON_NAME].preferences
    return preferences

def get_directory():
    preferences = get_preferences()
    return preferences.directory

def get_blender_version():
    preferences = get_preferences()
    return preferences.blenderVersion