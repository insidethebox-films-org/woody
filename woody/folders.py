import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .preferences import *

_json_cache = None

def create_folders_subfolders(folders, base_path):
    for main_folder, subfolders in folders.items():
        main_path = base_path / main_folder
        main_path.mkdir(parents=True, exist_ok=True)

        if isinstance(subfolders, dict):
            create_folders_subfolders(subfolders, main_path)
        elif isinstance(subfolders, list): 
            for subfolder in subfolders:
                (main_path / subfolder).mkdir(parents=True, exist_ok=True)

def create_default_proj_config(path: Path):
    default_config = {
        "render_settings": {
            "resolution_x": 1920,
            "resolution_y": 1080,
            "fps": 24,
            "file_format": "OPEN_EXR_MULTILAYER",
            "color_mode": "RGBA",
            "color_depth": "16",
            "compression": 15,
            "quality": 90,
            "exr_codec": "DWAA",
            "engine": "CYCLES",
            "use_motion_blur": True,
            "motion_blur_shutter": 0.5,
            "film_transparent": True,
            "use_simplify": True,
            "simplify_subdivision": 2,
            "simplify_subdivision_render": 5,
            "cycles_samples": 512,
            "use_persistent_data": True,
        }
    }

    config_path = path / "projConfig.json"
    with config_path.open("w") as f:
        json.dump(default_config, f, indent=2)

# Create enums based on json

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

def get_root_folders(self, context):
    data = load_json_data(context)
    items = [("NONE", "None", "No selection")]
    items += [(key, key, f"Root folder: {key}") for key, value in data.items() if value.get("type") == "root"]
    return items

def get_group_folders(self, context):
    data = load_json_data(context)
    items = [("NONE", "None", "No selection")]

    root_folder = context.scene.woody.root_folder
    root_data = data.get(root_folder)
    if not root_data or "contents" not in root_data:
        return items

    for key, value in root_data["contents"].items():
        if value.get("type") == "group":
            items.append((key, key, f"Group folder: {key}"))
    return items

def get_asset_folders(self, context):
    data = load_json_data(context)
    items = [("NONE", "None", "No selection")]

    props = context.scene.woody
    root_data = data.get(props.root_folder)
    if not root_data:
        return items

    group_data = root_data.get("contents", {}).get(props.group_folder)
    if not group_data or "contents" not in group_data:
        return items

    for key, value in group_data["contents"].items():
        if value.get("type") == "asset":
            items.append((key, key, f"Asset folder: {key}"))
    return items

def get_type_folders(self, context):
    data = load_json_data(context)
    items = [("NONE", "None", "No selection")]

    props = context.scene.woody
    root_data = data.get(props.root_folder)
    if not root_data:
        return items

    group_data = root_data.get("contents", {}).get(props.group_folder)
    if not group_data:
        return items

    asset_data = group_data.get("contents", {}).get(props.asset_folder)
    if not asset_data or "contents" not in asset_data:
        return items

    for key, value in asset_data["contents"].items():
        if value.get("type") == "type":
            items.append((key, key, f"Type folder: {key}"))
    return items

# Generate and save json folder structure

# ??? Should we still exclude _publish ???
def get_folder_structure(base_path, depth=0, exclude_names=("_publish",)):
    folder_dict = {}

    for item in os.listdir(base_path):
        if item in exclude_names:
            continue

        item_path = os.path.join(base_path, item)

        if os.path.isdir(item_path):
            folder_dict[item] = {
                "type": get_folder_type(depth),
                "contents": get_folder_structure(item_path, depth + 1, exclude_names)
            }

    return folder_dict

def get_folder_type(depth):
    if depth == 0:
        return "root"
    elif depth == 1:
        return "group"
    elif depth == 2:
        return "asset"
    else:
        return "type"

def save_structure_to_json(base_path):

    folder_structure = get_folder_structure(base_path)


    output_file = os.path.join(base_path, "projStruc.json")

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(folder_structure, json_file, indent=4)

    print(f"Folder structure saved to: {output_file}")

    global _json_cache
    _json_cache = None