import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .preferences import *

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
