import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

def generate_uuid_from_name(name):
    # Generate a UUID based on the collection name (with underscores replaced by slashes)
    collection_path = name.replace('_', '/')
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, collection_path))

def add_to_catalog_file(collection_name, file_path):
    try:
        # Generate UUID from collection name
        collection_uuid = generate_uuid_from_name(collection_name)
        
        # Correct the catalog entry to avoid double "assets/"
        collection_path = collection_name.replace('_', '/')
        catalog_entry = f"{collection_uuid}:{collection_path}:\n"
        
        # Check if the file exists, if not, create a new one with version line
        if not os.path.exists(file_path):
            with open(file_path, 'w') as cat_file:
                cat_file.write("VERSION 1\n")
        
        # Read the existing file and check for duplicates
        with open(file_path, 'r') as cat_file:
            lines = cat_file.readlines()
            if any(catalog_entry.strip() == line.strip() for line in lines):
                print(f"Entry already exists: {catalog_entry.strip()} - Skipping")
                return
        
        # Append the catalog entry to the file if it's not a duplicate
        with open(file_path, 'a') as cat_file:
            cat_file.write(catalog_entry)
            print(f"Added catalog entry: {catalog_entry.strip()}")
        
        return collection_uuid  # Return UUID so it can be added to the collection
    
    except PermissionError as e:
        print(f"❌ PermissionError: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return None

# ALL DEPRECATED