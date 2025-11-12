from .....database.db_instance import DB_instance

def get_blends_list(new_browser_selection):
    
    """
    Get list of blend files for the selected element
    
    Returns:
        tuple: (blends_list, element_id) or (None, None) if not found
    """
    
    if len(new_browser_selection) < 3:
        return None, None
    
    if not new_browser_selection.get("element"):
        return None, None
    
    root = new_browser_selection.get("group_type")
    group = new_browser_selection.get("group")
    element = new_browser_selection.get("element")
    
    if root == "Assets Group":
        collection_name = "assets"
        id_field = "asset_id"
    else:
        collection_name = "shots"
        id_field = "shot_id"
        
    element_id = DB_instance().get_docs(
        collection=collection_name, 
        key=["group", "name"],
        value=[group, element], 
        key_filter=id_field,
        find_one=True
    )
    
    if not element_id:
        return None, None
    
    blends = DB_instance().get_docs(
        collection="blends",
        key=["element_id"],
        value=[element_id],
        key_filter="name"
    )
    
    blends_sorted = sorted(blends, key=str.lower) if blends else []
    
    return blends_sorted, element_id


def get_blend_versions_list(element_id, selected):
    
    """
    Get versions for a specific blend file
    
    Args:
        element_id: The element ID from get_blends_list()
        selected: The selected blend name
        
    Returns:
        List of version strings sorted with "latest" first
    """
    
    if not element_id:
        return []
    
    versions_doc = DB_instance().get_docs(
        collection="blends",
        key=["element_id", "name"],
        value=[element_id, selected],
        find_one=True
    )

    blend_versions_dict = versions_doc.get("blend_files", {}) if versions_doc else {}
    versions = list(blend_versions_dict.values())
    
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