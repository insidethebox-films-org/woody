from ....tool.woody_instance import WoodyInstance

import subprocess
import os

def open_blend_file(executable: str, blend_path: str, addon_zip: str) -> bool:
    """
    Opens existing blend file with addon update check and sets preferences
    
    Args:
        executable (str): Path to Blender executable
        blend_path (str): Path to the blend file to open
        addon_zip (str): Path to the addon zip file
        
    Returns:
        bool: True if blend file was opened successfully
    """

    try:
        woody_instance = WoodyInstance()
        mongo_address = woody_instance.mongoDBAddress or ""
        project_name = woody_instance.projectName or ""
        
        blend_path = str(blend_path)
        blend_dir = os.path.dirname(blend_path)
        startup_path = os.path.join(blend_dir, "_woody_startup.py")

        startup_script = f"""
import bpy
import addon_utils
import os
import hashlib
import json
import shutil

addon_name = "woody_blender_addon"
zip_path = r"{addon_zip}"

# Get current hash
def get_zip_hash(zip_path):
    if not os.path.exists(zip_path):
        return ""
    with open(zip_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

current_hash = get_zip_hash(zip_path)

# Get stored hash
prefs_path = os.path.join(bpy.utils.user_resource('CONFIG'), "woody_addon_hash.json")
stored_hash = ""
if os.path.exists(prefs_path):
    try:
        with open(prefs_path, 'r') as f:
            stored_hash = json.load(f).get('hash', '')
    except:
        pass

addons_path = bpy.utils.user_resource('SCRIPTS', path="addons")
addon_folder = os.path.join(addons_path, addon_name)
addon_exists = os.path.exists(addon_folder)

# Update if hash changed OR addon doesn't exist
if current_hash != stored_hash or not addon_exists:
    print(f"Updating {{addon_name}}...")
    print(f"  Reason: {{'Hash changed' if current_hash != stored_hash else 'Addon not installed'}}")
    
    # Disable addon if currently enabled
    if addon_name in bpy.context.preferences.addons:
        try:
            addon_utils.disable(addon_name)
        except:
            pass
    
    # Remove from sys.modules to force reload
    import sys
    for key in list(sys.modules.keys()):
        if key.startswith(addon_name):
            del sys.modules[key]
    
    # Remove old addon folder
    if addon_exists:
        try:
            shutil.rmtree(addon_folder)
            print(f"  Removed old addon folder")
        except Exception as e:
            print(f"  Warning: Could not remove old folder: {{e}}")
    
    # Install new addon
    try:
        bpy.ops.preferences.addon_install(overwrite=True, target='DEFAULT', filepath=zip_path)
        addon_utils.enable(addon_name, default_set=True, persistent=True)
        
        # Store new hash
        os.makedirs(os.path.dirname(prefs_path), exist_ok=True)
        with open(prefs_path, 'w') as f:
            json.dump({{'hash': current_hash}}, f)
        
        print(f"Addon installed and enabled")
    except Exception as e:
        print(f"  Error installing addon: {{e}}")
        import traceback
        traceback.print_exc()
else:
    print(f"Addon {{addon_name}} is up to date")

# Always ensure addon is enabled
if addon_name not in bpy.context.preferences.addons:
    try:
        addon_utils.enable(addon_name, default_set=True, persistent=True)
        print(f"Addon enabled")
    except Exception as e:
        print(f"  Warning: Could not enable addon: {{e}}")

# Set preferences
try:
    addon_prefs = bpy.context.preferences.addons["woody_blender_addon"].preferences
    addon_prefs.mongodb_address = "{mongo_address}"
    addon_prefs.project_name = "{project_name}"
    bpy.ops.wm.save_userpref()
    print(f"Preferences set")
except Exception as e:
    print(f"  Error setting preferences: {{e}}")

# Clean up startup script
try:
    os.remove(__file__)
except:
    pass
"""

        os.makedirs(blend_dir, exist_ok=True)
        with open(startup_path, 'w', encoding='utf-8') as f:
            f.write(startup_script)
        
        subprocess.Popen([
            executable,
            str(blend_path),
            "--python", startup_path 
        ])

        return True
    
    except Exception as e:
        print(f"Error opening blend file: {e}")
        return False