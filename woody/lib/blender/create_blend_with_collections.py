import bpy
import os

from pathlib import Path

from ...preferences import *
from ...utils.context import *

def create_blend_with_collection(file_name, collection_name, target_directory): 

    # Ensure the target directory exists
    target_dir = Path(target_directory)
    os.makedirs(target_dir, exist_ok=True)

    file_path = target_dir / file_name
    file_path_str = str(file_path)

    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"❌ Collection '{collection_name}' not found in current file.")
        return

    # Recursively gather all collections
    def gather_collections(col, seen=None):
        if seen is None:
            seen = set()
        seen.add(col)
        for child in col.children:
            if child not in seen:
                gather_collections(child, seen)
        return seen

    collections = gather_collections(collection)
    
    # Gather all objects in all collections
    objects = set()
    for col in collections:
        for obj in col.objects:
            objects.add(obj)

    # Gather meshes and materials used by objects
    meshes = {obj.data for obj in objects if obj.type == 'MESH' and obj.data}
    materials = {mat for obj in objects if obj.type == 'MESH' for mat in obj.data.materials if mat}

    datablocks = {collection} | collections | objects | meshes | materials

    try:
        bpy.data.libraries.write(
            file_path_str,
            datablocks,
            fake_user=True,
            compress=True
        )
        print(f"✅ Exported: '{collection_name}' with {len(objects)} object(s), {len(meshes)} mesh(es), {len(materials)} material(s)")
    except Exception as e:
        print(f"❌ Failed to export collection: {e}")