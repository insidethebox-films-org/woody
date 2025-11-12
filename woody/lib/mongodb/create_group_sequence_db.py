from ...tool import WoodyInstance
from ...database.db_instance import DB_instance
from ...database.templates.groups import groups_template
from ...database.templates.sequences import sequences_template

import copy
from datetime import datetime, timezone

def create_group_sequence_db(type, name):

    db = DB_instance()

    if type == 'Assets Group':
        collection_name = "groups"
        template_type = groups_template
        element_type = "assets"

    else:
        collection_name = "sequences"
        template_type = sequences_template
        element_type = "shots"
    
    # Check if document with the same name already exists
    if db.connect[collection_name].find_one({"name": name}):
        print(f"Document '{name}' already exists in collection '{collection_name}'.")
        return

    #Create collection if it doesn't exist
    db.add_collection(collection_name)
    #Create document from template
    template = copy.deepcopy(template_type)
    template["name"] = name
    template[element_type] = {}
    template["created_time"] = datetime.now(timezone.utc)  
    template["modified_time"] = datetime.now(timezone.utc)
    
    db.add_document(collection_name, template)
    print(f"Document '{name}' is set up in collection '{collection_name}'.")

