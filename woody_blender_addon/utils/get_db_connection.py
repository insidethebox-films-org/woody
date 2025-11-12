import bpy
from pymongo import MongoClient

def get_database_connection():
    """Get MongoDB database connection from addon preferences"""
    try:
        addon_prefs = bpy.context.preferences.addons["woody_blender_addon"].preferences
        
        mongo_url = addon_prefs.mongodb_address
        project_name = addon_prefs.project_name
        
        if not mongo_url or not project_name:
            return None, None, "MongoDB address or project not configured"
        
        client = MongoClient(mongo_url)
        db = client[project_name]
        
        return client, db, None
        
    except Exception as e:
        return None, None, str(e)