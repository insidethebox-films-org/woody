import bpy

def get_preferences():
    try:
        return bpy.context.preferences.addons["woody"].preferences
    except KeyError:
        return None

def get_directory():
    prefs = get_preferences()
    return prefs.directory if prefs else ""

def get_blender_version():
    prefs = get_preferences()
    return prefs.blenderVersion if prefs else ""