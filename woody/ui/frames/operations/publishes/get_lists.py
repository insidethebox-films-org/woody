from .....database.db_instance import DB_instance
import os
from ....utils.load_icon import load_icon


def get_publishes_list(new_browser_selection):
    
    if len(new_browser_selection) < 3:
        return []
    
    if not new_browser_selection.get("element"):
        return []
    
    element = new_browser_selection.get("element")
    
    publishes_docs = DB_instance().get_docs(
        collection="publishes", 
        key=["source_asset"],
        value=[element]
    )
    
    if not publishes_docs:
        return []
    
    publishes_list = []
    
    icon_map = {
        "COLLECTION": "collection",
        "MATERIAL": "material",
        "NODE_GROUP": "node_group",
        "OBJECT": "object"
    }
    
    for doc in publishes_docs:
        publish_name = doc.get("custom_name", "Unknown")
        publish_type = doc.get("publish_type", "OBJECT")
        image_type = icon_map.get(publish_type, "object")
        
        image_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "..", "..", 
            "icons", "publishes", 
            f"{image_type}.png"
        )
        
        icon = None
        if os.path.exists(image_path):
            try:
                icon = load_icon(image_path, 20)
            except Exception as e:
                print(f"Error loading icon for {publish_name}: {e}")
        
        publishes_list.append({
            "name": publish_name,
            "type": publish_type,
            "icon": icon
        })

    publishes_list.sort(key=lambda x: x["name"].lower())
    
    return publishes_list


def get_publish_versions_list(selected_publish_name):
    
    if not selected_publish_name:
        return []
    
    versions = DB_instance().get_nested_keys(
        collection="publishes",
        key="custom_name",
        value=selected_publish_name,
        field_name="published_versions"
    )
    
    if not versions:
        return []
    
    def sort_versions(v):
        if v == "latest":
            return (0, 0) 
        else:
            try:
                num = int(v) 
                return (1, -num)
            except ValueError:
                return (2, v)
    
    versions_sorted = sorted(versions, key=sort_versions)
    
    return versions_sorted