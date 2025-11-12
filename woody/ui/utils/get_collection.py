def get_collection(group_type, type=""):
    
    if not group_type:
        print("Error: Need to pick a selection")
        return None, None
    
    if not type:
        print("Error: No collection type group_type")
        return None, None
    
    if type == "group":
        if group_type == "Assets Group":
            collection_name = "groups"
        else:
            collection_name = "sequences"
        
        return collection_name

    if type == "element":
        if group_type == "Assets Group":
            collection_name = "assets"
            key_type = "group" 
        else:
            collection_name = "shots"
            key_type = "sequence"
        
        return collection_name, key_type 
    
    return None, None