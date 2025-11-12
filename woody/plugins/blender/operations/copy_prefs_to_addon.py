import shutil
from pathlib import Path

def copy_prefs_to_addon():
    """Copy prefs.json to the woody_blender_addon folder"""
    try:
        # Source: main prefs.json
        source_prefs = Path("prefs/prefs.json")
        
        # Destination: addon prefs.json
        addon_prefs_dir = Path("woody_blender_addon/prefs")
        addon_prefs_dir.mkdir(exist_ok=True)
        dest_prefs = addon_prefs_dir / "prefs.json"
        
        # Copy the file
        shutil.copy2(source_prefs, dest_prefs)
        print(f"✓ Copied preferences to addon: {dest_prefs}")
        
    except Exception as e:
        print(f"Error copying prefs to addon: {str(e)}")