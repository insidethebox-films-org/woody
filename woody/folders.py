import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .preferences import *

def create_folders_subfolders(folders, base_path):
    for main_folder, subfolders in folders.items():
        main_path = base_path / main_folder
        main_path.mkdir(parents=True, exist_ok=True)

        if isinstance(subfolders, dict):
            create_folders_subfolders(subfolders, main_path)
        elif isinstance(subfolders, list): 
            for subfolder in subfolders:
                (main_path / subfolder).mkdir(parents=True, exist_ok=True)

# Create enums based on json

def load_json_data(context):
    global _json_cache
    if _json_cache is None:
        print("================= Loading new JSON data... =================")
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
    print("Using cached JSON.")
    return _json_cache

def get_root_folders(self, context):
    data = load_json_data(context)
    return [(key, key, f"Root folder: {key}") for key, value in data.items() if value.get("type") == "root"] or [("NONE", "None", "No root folders found")]

def get_group_folders(self, context):
    data = load_json_data(context)
    selected_root = context.scene.woody.root_folder

    if selected_root not in data:
        return [("NONE", "None", "No groups found")]

    root_contents = data[selected_root]["contents"]
    return [(key, key, f"Group: {key}") for key, value in root_contents.items() if value.get("type") == "group"] or [("NONE", "None", "No groups found")]

def get_asset_folders(self, context):
    data = load_json_data(context)
    selected_root = context.scene.woody.root_folder
    selected_group = context.scene.woody.group_folder

    if selected_root not in data:
        return [("NONE", "None", "No assets found")]

    group_contents = data[selected_root]["contents"].get(selected_group, {}).get("contents", {})
    return [(key, key, f"Asset: {key}") for key, value in group_contents.items() if value.get("type") == "asset"] or [("NONE", "None", "No assets found")]

def get_type_folders(self, context):
    data = load_json_data(context)
    selected_root = context.scene.woody.root_folder
    selected_group = context.scene.woody.group_folder
    selected_asset = context.scene.woody.asset_folder

    if selected_root not in data:
        return [("NONE", "None", "No types found")]

    asset_contents = data[selected_root]["contents"].get(selected_group, {}).get("contents", {}).get(selected_asset, {}).get("contents", {})
    return [(key, key, f"Type: {key}") for key, value in asset_contents.items() if value.get("type") == "type"] or [("NONE", "None", "No types found")]

# Generate and save json folder structure

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
