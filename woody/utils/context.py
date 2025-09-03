import bpy
from pathlib import Path

def context_names():
    if not bpy.data.filepath:
        print("[context_names] 🚨 No filepath set — save your .blend file first.")
        return "ROOT", "GROUP", "ASSET", "TYPE"
     
    current_path = Path(bpy.data.filepath)
    directory = current_path.parent
    directory = directory.parts

    if len(directory) < 4:
       print(f"[context_names] 🚨 Not enough directories in path: {directory}")
       return "ROOT", "GROUP", "ASSET", "TYPE"

    root = directory[-4]
    group = directory[-3]
    asset = directory[-2]
    type_ = directory[-1]

    return root, group, asset, type_