import bpy

_addon_key_cache = None

def get_addon_key():
    global _addon_key_cache
    if _addon_key_cache:
        return _addon_key_cache

    current_name = __name__
    for addon_key in bpy.context.preferences.addons.keys():
        if current_name.startswith(addon_key):
            _addon_key_cache = addon_key
            return addon_key

    print(f"[Woody] Could not determine addon key for __name__: {__name__}")
    return None

def get_preferences():
    addon_key = get_addon_key()
    if not addon_key:
        return None
    return bpy.context.preferences.addons[addon_key].preferences

def get_directory():
    prefs = get_preferences()
    return prefs.directory if prefs else ""

def get_blender_version():
    prefs = get_preferences()
    return prefs.blenderVersion if prefs else ""


class Preferences_Properties:
    directory: bpy.props.StringProperty(
        name="Directory",
        subtype='FILE_PATH',
        description="The directory of your project"
    ) # type: ignore
    blenderVersion: bpy.props.StringProperty(
        name="EXE Path",
        subtype='FILE_PATH',
        description="Path to your blender.exe"
    ) # type: ignore
