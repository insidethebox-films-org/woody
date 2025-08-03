import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

ADDON_NAME = 'woody'

class Preferences_Properties:
    directory: bpy.props.StringProperty(name= "Directory", subtype='FILE_PATH', description="The directory of your project") # type: ignore
    blenderVersion: bpy.props.StringProperty(name= "EXE Path", subtype='FILE_PATH', description="Path to your blender.exe") # type: ignore

def get_preferences():
    preferences = bpy.context.preferences.addons[ADDON_NAME].preferences
    return preferences

def get_directory():
    preferences = get_preferences()
    return preferences.directory

def get_blender_version():
    preferences = get_preferences()
    return preferences.blenderVersion