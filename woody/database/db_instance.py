from ..tool import WoodyInstance
from pymongo import MongoClient
from pathlib import Path


class DB_instance:
    def __init__(self, name=None):
        self.client = self.get_mongo_client()
        self.name = self.get_project_name() if name is None else name
        self.connect = self.client[self.name] if self.name else None
        self.collections = self.get_collections_from_db()  # Dictionary to store multiple collections
        self.projectDirectory = Path(self.get_project_directory()) if self.get_project_directory() else None
        
    def get_mongo_client(self):
        woody = WoodyInstance()
        return MongoClient(woody.mongoDBAddress)

    def get_project_name(self):
        return WoodyInstance().projectName
    
    def get_collections_from_db(self):
        if self.connect is not None:
            return {name: self.connect[name] for name in self.connect.list_collection_names()}
        else:
            return {}
        
    def get_project_directory(self):
        if self.connect is not None:
            settings = self.connect['settings'].find_one({})
            if settings and 'location' in settings:
                path_str = settings['location']
                return path_str
        return None
        
    def add_collection(self, collection_name):
        if self.connect is not None:
            self.collections[collection_name] = self.connect[collection_name]
        else:
            raise Exception("No database selected")

    def add_document(self, collection_name, doc):
        if collection_name in self.collections:
            result = self.collections[collection_name].insert_one(doc)
            return result.inserted_id
        else:
            raise Exception(f"Collection '{collection_name}' not found")  
    
    def update_document(self, collection_name, query, update):
        if collection_name in self.collections:
            result = self.collections[collection_name].update_one(query, update)
            return result.modified_count
        else:
            raise Exception(f"Collection '{collection_name}' not found")
        
    def get_docs(self, collection, key=[], value=[], key_filter=None, find_one=False):
        
        """
        Args:
            collection: Collection name
            key: List of field names to filter by
            value: List of values to match
            key_filter: If provided, return only this field from matched docs
            find_one: If True, return single document; if False, return list
        
        Returns:
            Documents, field values, or None/[] if not found
        """
        
        if self.connect is None:
            return None if find_one else []
        
        try:
            query = {}
            if key and value:
                for i in range(min(len(key), len(value))):
                    query[key[i]] = value[i]
            
            # Return specific fields from documents
            if key_filter:
                if find_one:
                    doc = self.connect[collection].find_one(query)
                    if doc and key_filter in doc:
                        return doc[key_filter]
                    return None
                else:
                    filtered_docs = list(self.connect[collection].find(query))
                    values = [item[key_filter] for item in filtered_docs if key_filter in item]
                    return values
            
            # Return full documents
            if find_one:
                doc = self.connect[collection].find_one(query)
                return doc
            else:
                filtered_docs = list(self.connect[collection].find(query))
                return filtered_docs
                
        except Exception as e:
            print(f"Database query error: {e}")
            return None if find_one else []
        
    def get_nested_keys(self, collection, key, value, field_name):
        """Get keys from a nested dictionary field in a document"""
        try:
            doc = self.connect[collection].find_one({key: value})
            
            if doc and field_name in doc:
                field_value = doc[field_name]
                if isinstance(field_value, dict):
                    return list(field_value.keys())
            
            return []
        except Exception as e:
            print(f"Error getting nested keys: {e}")
            return []



        