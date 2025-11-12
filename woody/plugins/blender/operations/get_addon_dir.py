import os
import platform
from pathlib import Path

def get_addon_dir(blender_executable):
        
        dev_addon_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../woody_blender_addon"))
        if os.path.exists(dev_addon_dir):
            return dev_addon_dir
        
        if not blender_executable:
            return None
        
        blender_base = Path(blender_executable)
        system = platform.system()
        
        if system == "Windows":
            addon_dir = blender_base / "portable" / "scripts" / "addons" / "woody_blender_addon"
            
        elif system == "Darwin":
            if blender_base.name.endswith(".app"):
                blender_base = blender_base / "Contents" / "Resources"
            
            version_dir = next(blender_base.glob("*.*"), None)
            if not version_dir:
                return None
            
            addon_dir = version_dir / "scripts" / "addons" / "woody_blender_addon"
                    
        else:
            version_dir = next(blender_base.glob("*.*"), None)
            if not version_dir:
                return None
            
            addon_dir = version_dir / "scripts" / "addons" / "woody_blender_addon"
        
        return str(addon_dir)