from .load_save_json_data import load_json_data

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