import os
import subprocess
import bpy
import json
from pathlib import Path

def new_blend(blender_exe, new_file_name, collection_name, config_path):

    blender_exe_path = Path(blender_exe)
    if not blender_exe_path.exists():
        print(f"❌ Error: Blender executable not found at {blender_exe}")
        return

    # ??? is this else needed, or is there logic to avoid it ???
    if bpy.data.filepath:
        current_directory = Path(bpy.path.abspath("//"))
    else:
        current_directory = Path(os.path.expanduser("~")) / "Blender_New_Files"
        current_directory.mkdir(parents=True, exist_ok=True)

    new_file_path = current_directory / new_file_name

    frame_start = 0  # Default Value for both Asset and Shot, should match default config
    frame_end = 100 # Default Value for both Asset and Shot, should match default config
    if config_path and Path(config_path).exists():
        with open(config_path, "r") as f:
            config_data = json.load(f)
            frame_start = config_data.get("frame_start", 0)
            frame_end = config_data.get("frame_end", 100)

    python_expr = f"""
import bpy
bpy.data.collections['Collection'].name = '{collection_name}'
bpy.context.scene.frame_start = {frame_start}
bpy.context.scene.frame_end = {frame_end}
bpy.ops.wm.save_mainfile(filepath=r'{new_file_path}')
"""

    command = [
        str(blender_exe_path),
        "--background",
        "--python-expr", python_expr
    ]

    subprocess.Popen(command)

    open_command = [
        str(blender_exe_path),
        str(new_file_path)
    ]

    subprocess.Popen(open_command)

    print(f"Opening new Blender instance with file: {new_file_path}")