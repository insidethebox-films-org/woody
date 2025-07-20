import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .preferences import *
from .context import *

def create_blend_with_collection(file_name, collection_name, target_directory): 
    from pathlib import Path
    import bpy
    import os

    # Ensure the target directory exists
    target_dir = Path(target_directory)
    os.makedirs(target_dir, exist_ok=True)

    file_path = target_dir / file_name
    file_path_str = str(file_path)

    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"❌ Collection '{collection_name}' not found in current file.")
        return

    # #Get all objects inside the collection
    # objects = {obj for obj in collection.all_objects}

    # #Optionally gather mesh, materials, etc.
    # meshes = {obj.data for obj in objects if obj.type == 'MESH' and obj.data}
    # materials = {mat for obj in objects if obj.type == 'MESH' for mat in obj.data.materials if mat}
    
    datablocks = {collection} #| objects | meshes | materials

    try:
        bpy.data.libraries.write(
            file_path_str,
            datablocks,
            fake_user=True,
            compress=True
        )
        #print(f"✅ Exported: '{collection_name}' with {len(objects)} object(s), {len(meshes)} mesh(es), {len(materials)} material(s)")
    except Exception as e:
        print(f"❌ Failed to export collection: {e}")

def open_publish_blend_file(file_path):

    blender_exe = get_blender_version()

    if not os.path.exists(file_path):
        print(f"❌ Error: File does not exist - {file_path}")
        return

    subprocess.Popen([blender_exe, file_path], close_fds=True, start_new_session=True)

    print(f"✅ Opened Blender in a separate instance with file: {file_path}")

def show_popup_message(message, title="Info", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def set_render_output_to_cg():
    if not bpy.data.filepath:
        print("[set_render_output_to_cg] 🚨 File not saved yet.")
        return False

    root, group, asset, type_ = context_names()

    # Validate structure
    if root not in {"assets", "shots"} or group == "GROUP" or asset == "ASSET":
        print(f"[set_render_output_to_cg] 🚨 Unexpected path: {root}/{group}/{asset}")
        return False

    current_path = Path(bpy.data.filepath)

    # Fix: Avoid duplicating the root folder in path
    cg_folder = current_path.parents[3] / group / asset / "cg"

    # Create folder if needed
    cg_folder.mkdir(parents=True, exist_ok=True)

    # 🆕 Get next version folder inside cg/
    version_folder = get_next_version_folder(cg_folder)
    version_folder.mkdir(parents=True, exist_ok=True)

    # Set output path
    bpy.context.scene.render.filepath = str(version_folder) + "/"
    print(f"[set_render_output_to_cg] ✅ Output path set to {bpy.context.scene.render.filepath}")
    return True

def get_next_version_folder(base_path):
    version_pattern = re.compile(r"v(\d+)")
    versions = []

    for item in base_path.iterdir():
        if item.is_dir():
            match = version_pattern.fullmatch(item.name)
            if match:
                versions.append((int(match.group(1)), item))

    if not versions:
        return base_path / "v1"

    # Sort by version number descending
    versions.sort(reverse=True)
    latest_version_num, latest_version_path = versions[0]

    # Check if the latest version folder has any files inside
    if any(latest_version_path.iterdir()):
        # Folder is not empty → increment version
        return base_path / f"v{latest_version_num + 1}"
    else:
        # Folder is empty → reuse it
        return latest_version_path
