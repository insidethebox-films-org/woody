from ...database.db_instance import DB_instance

def get_projects_db():
    
    db = DB_instance()
    
    # Return empty list if no MongoDB address is configured
    if not db.client:
        return []
    try:
        db_list = db.client.list_database_names()
        return [db for db in db_list if db not in ['admin', 'config', 'local']]
    except Exception as e:
        # Return empty list if connection fails
        print(f"Failed to connect to MongoDB: {e}")
        return []

