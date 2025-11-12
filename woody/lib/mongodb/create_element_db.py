from ...tool import WoodyInstance
from ...database.db_instance import DB_instance
from ...database.templates.assets import assets_template
from ...database.templates.shots import shots_template
from ...utils import generate_uuid

import copy
from datetime import datetime, timezone

def create_element_db(groupTypeCombo, groupName, elementName):

    db = DB_instance()

    if groupTypeCombo == 'Assets Group':
        collection_name = "assets"
        group_type = "group"
        template_type = assets_template
        id_type = "asset_id"

    else:
        collection_name = "shots"
        group_type = "sequence"
        template_type = shots_template
        id_type = "shot_id"

    # Check if document with the same name already exists
    if db.connect[collection_name].find_one({"name": elementName, group_type: groupName}):
        print(f"Document '{elementName}' already exists in collection '{collection_name}'.")
        return
    
    #Create collection if it doesn't exist
    db.add_collection(collection_name)

    #Create document from template
    template = copy.deepcopy(template_type)
    template[id_type] = generate_uuid()
    template[group_type] = groupName
    template["name"] = elementName
    template["latest_version"] = None
    template["created_time"] = datetime.now(timezone.utc)  
    template["modified_time"] = datetime.now(timezone.utc)

    db.add_document(collection_name, template)
    print(f"Document '{elementName}' is set up in collection '{collection_name}'.")

    #Update the group or sequence document to include the new element
    group_collection_name = group_type + "s" #groups or sequences #TODO Take a look at removing this
    query = {"name": groupName}
    attribute = collection_name
    update = {"$set": {f"{attribute}.{elementName}": template[id_type]}}
    db.update_document(group_collection_name, query, update)

    print(f"Document '{elementName}' added to '{group_collection_name}' document '{groupName}'.")
