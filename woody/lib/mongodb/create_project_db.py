from ...database.db_instance import DB_instance
from ...database.templates.settings import settings_template

import copy
from datetime import datetime, timezone

def create_project_db(name, host_address, directory):
    
    db = DB_instance(name)

    # Check if collection 'settings' already exists
    if "settings" in db.collections:
        print(f"Collection 'settings' already exists in database '{name}'.")
        return False
    
    #Create 'settings' collection
    db.add_collection("settings")
    
    settings = copy.deepcopy(settings_template)
    settings["project_name"] = name
    settings["host_address"] = host_address
    settings["location"] = directory
    settings["created_time"] = datetime.now(timezone.utc)
    db.add_document("settings", settings)

    print(f"Collection 'settings' is set up in database '{db.name}'.")
    return True

    

