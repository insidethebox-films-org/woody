import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path
from .context import *
from .utils import *

def new_blend(blender_exe, new_file_name, collection_name):

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

   

    python_expr = f"""
import bpy
bpy.data.collections['Collection'].name = '{collection_name}'
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

def open_blend(blender_exe, blend_file_path):
    blender_exe_path = Path(blender_exe)
    blend_file = Path(blend_file_path)

    if not blender_exe_path.exists():
        print(f"❌ Error: Blender executable not found at {blender_exe}")
        return

    if not blend_file.exists():
        print(f"❌ Error: .blend file not found at {blend_file_path}")
        return

    subprocess.Popen([str(blender_exe_path), str(blend_file)])

    print(f"Opening new Blender instance with file: {blend_file_path}")

def save_current_scene():

    if bpy.data.filepath:
        bpy.ops.wm.save_mainfile()
        print(f"Scene saved: {bpy.data.filepath}")
    else:
        print("Scene has not been saved before. Skipping save.")

def incremental_save(new_name):
    
    if not bpy.data.filepath:
        print("❌ Error: Scene has not been saved before. Save it first.")
        return
    
    current_path = Path(bpy.data.filepath)
    directory = current_path.parent
    extension = current_path.suffix

    print("Checking files in directory:", directory)

    version_pattern = re.compile(rf"{re.escape(new_name)}_v(\d+){re.escape(extension)}$")

    existing_versions = []
    for file in directory.iterdir():
        match = version_pattern.match(file.name)
        if match:
            existing_versions.append(int(match.group(1)))

    print("Existing versions found:", existing_versions)

    next_version = max(existing_versions, default=0) + 1

    new_filename = f"{new_name}_v{next_version}{extension}"
    new_file_path = directory / new_filename

    shutil.copy2(current_path, new_file_path)

    print(f"Duplicated and renamed scene as: {new_file_path}")

def restart_blend_file():

    current_file = bpy.data.filepath

    if not current_file:
        print("No file is currently open.")
        return
    
    bpy.ops.wm.open_mainfile(filepath=current_file)
