import os
import platform

def set_executable_path(base_path: str) -> str:
    """
    Sets the correct Blender executable path based on platform
    
    Args:
        base_path: Base Blender installation path
                   Windows: "D:\_software\blender-4.2.5-windows-x64"
                   macOS: "/Applications/Blender.app"
    
    Returns:
        Full path to Blender executable
    """
    system = platform.system()
    
    if system == "Darwin":
        if base_path.endswith(".app"):
            return os.path.join(base_path, "Contents", "MacOS", "Blender")
        elif "MacOS" in base_path and base_path.endswith("Blender"):
            return base_path
        else:
            return os.path.join(base_path, "Contents", "MacOS", "Blender")
    
    elif system == "Windows":
        return os.path.join(base_path, "blender.exe")
    
    elif system == "Linux":
        return os.path.join(base_path, "blender")
    
    else:
        raise Exception(f"Unsupported platform: {system}")