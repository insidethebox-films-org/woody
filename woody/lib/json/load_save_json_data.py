from ...preferences import *
from ..folders import get_folder_structure

import bpy
import os
import json
from pathlib import Path

_json_cache = None

def load_json_data(context):
    global _json_cache
    if _json_cache is None:
        print("================= Loading new JSON data... =================")
        
        # ??? Is context needed, both scene and my_props are unused ???
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        base_path = Path(bpy.path.abspath(directory))
        json_file = base_path / "projStruc.json"

        if not json_file.exists():
            print("ERROR: JSON file not exist.")
            return {}

        with open(json_file, "r", encoding="utf-8") as file:
            _json_cache = json.load(file)
        print("================= CACHE LOADED =================")
        return _json_cache
    #print("Using cached JSON.")
    return _json_cache

def save_structure_to_json(base_path):

    folder_structure = get_folder_structure(base_path)


    output_file = os.path.join(base_path, "projStruc.json")

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(folder_structure, json_file, indent=4)

    print(f"Folder structure saved to: {output_file}")

    global _json_cache
    _json_cache = None