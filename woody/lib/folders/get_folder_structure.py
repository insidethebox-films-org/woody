from .get_folder_types import get_folder_type

import os

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