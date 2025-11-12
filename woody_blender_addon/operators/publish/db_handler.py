import uuid
from datetime import datetime, timezone
from pathlib import Path

from ...utils.get_db_connection import get_database_connection
from ...utils.publish_utils import to_project_relative
from ...utils.publish_utils import to_absolute_path

class PublishDatabaseHandler:
    """Handles database operations for publishing"""

    def get_existing_names_for_type(self, asset_name: str, publish_type: str):
        """Get list of existing custom names for this asset and type"""
        try:
            client, db, error = get_database_connection()
            if error or client is None or db is None:
                return []

            # Query for publishes matching this asset and type
            query = {
                "source_asset": asset_name,
                "publish_type": publish_type
            }
            
            publishes = list(db["publishes"].find(query))
            client.close()
            
            # Extract unique custom names
            custom_names = set()
            for pub in publishes:
                if "custom_name" in pub:
                    custom_names.add(pub["custom_name"])
            
            return sorted(list(custom_names))
            
        except Exception as e:
            print(f"Error getting existing names: {e}")
            return []

    def get_or_create_publish_document(self, source_asset: str, publish_type: str, custom_name: str):
        """Get existing publish document or create new one with the new structure"""
        try:
            client, db, error = get_database_connection()
            if error or client is None or db is None:
                return None, None

            query = {
                "source_asset": source_asset,
                "publish_type": publish_type,
                "custom_name": custom_name
            }
            
            existing = db["publishes"].find_one(query)
            
            if existing: #TODO Currently handles if existing document is old format - can be removed later
                # Convert old format to new format if needed
                if "published_versions" not in existing:
                    # This is an old format document - convert it
                    published_versions = {}
                    
                    # If it has the old structure, migrate it
                    if "published_path" in existing:
                        if existing.get("final_asset_name", "").endswith("_latest"):
                            published_versions["latest"] = {
                                "source_file": existing.get("source_file", ""),
                                "published_path": existing.get("published_path", ""),
                                "created_time": existing.get("created_time", datetime.now(timezone.utc)),
                                "selected_item": existing.get("selected_item", "")
                            }
                        else:
                            # Try to extract version number from final_asset_name
                            final_name = existing.get("final_asset_name", "")
                            if "_v" in final_name:
                                version = final_name.split("_v")[-1]
                                published_versions[version] = {
                                    "source_file": existing.get("source_file", ""),
                                    "published_path": existing.get("published_path", ""),
                                    "created_time": existing.get("created_time", datetime.now(timezone.utc)),
                                    "selected_item": existing.get("selected_item", "")
                                }
                    
                    # Update document to new format
                    db["publishes"].update_one(
                        {"_id": existing["_id"]},
                        {
                            "$set": {"published_versions": published_versions},
                            "$unset": {
                                "final_asset_name": "",
                                "published_path": "",
                                "source_file": "",
                                "selected_item": "",
                                "version": ""
                            }
                        }
                    )
                    existing["published_versions"] = published_versions
                
                client.close()
                return existing, db
            else:
                # Create new document with new structure
                new_document = {
                    "publish_id": str(uuid.uuid4()),
                    "source_asset": source_asset,
                    "publish_type": publish_type,
                    "custom_name": custom_name,
                    "published_versions": {},
                    "created_time": datetime.now(timezone.utc)
                }
                
                result = db["publishes"].insert_one(new_document)
                new_document["_id"] = result.inserted_id
                
                client.close()
                return new_document, db
            
        except Exception as e:
            print(f"Error getting/creating publish document: {e}")
            return None, None

    def get_next_version_number(self, publish_document):
        """Get the next version number from the published_versions in the document"""
        try:
            if not publish_document or "published_versions" not in publish_document:
                return 1
            
            published_versions = publish_document["published_versions"]
            
            # Find the highest numeric version
            max_version = 0
            for version_key in published_versions.keys():
                if version_key != "latest" and version_key.isdigit():
                    max_version = max(max_version, int(version_key))
            
            return max_version + 1
            
        except Exception as e:
            print(f"Error getting next version: {e}")
            return 1

    def version_latest_publish(self, publish_document, version_number: int):
        """Move the current 'latest' to a versioned entry within the same document"""
       
        try:
            client, db, error = get_database_connection()
            if error or client is None or db is None:
                return False, None

            published_versions = publish_document.get("published_versions", {})
            
            if "latest" not in published_versions:
                print("No 'latest' version found to version up")
                return False, None
            
            latest_version = published_versions["latest"]
            relative_published_path = latest_version["published_path"]
            absolute_published_path = to_absolute_path(relative_published_path)
            
            old_path = Path(absolute_published_path)
            
            # Check if the file actually exists
            if not old_path.exists():
                print(f"WARNING: File does not exist at {old_path}")
                # Continue anyway to update database
        
            # Generate new versioned filename
            old_name = old_path.stem  # filename without extension
            new_name = old_name.replace("_latest", f"_v{version_number}")
            new_path = old_path.parent / f"{new_name}.blend"

            print(f"Renaming file from {old_path} to {new_path}")
            
            # Rename the actual blend file
            if old_path.exists():
                old_path.rename(new_path)
                print(f"Renamed file: {old_path.name} -> {new_path.name}")
            
            # Move 'latest' to versioned entry and update the path (store as relative)
            versioned_entry = latest_version.copy()
            versioned_entry["published_path"] = to_project_relative(str(new_path))
            versioned_entry["versioned_time"] = datetime.now(timezone.utc)
            
            # Update the document: move latest to version number
            update_result = db["publishes"].update_one(
                {"_id": publish_document["_id"]},
                {
                    "$set": {f"published_versions.{version_number}": versioned_entry},
                    "$unset": {"published_versions.latest": ""}
                }
            )
            
            client.close()
            
            success = update_result.modified_count > 0
            return success, str(new_path) if success else None
            
        except Exception as e:
            print(f"Error versioning latest publish: {e}")
            return False, None
    
    def add_latest_version_to_document(self, publish_document, selected_item: str, published_path: str, source_file: str):
        """Add a new 'latest' version to the publish document"""
        try:
            client, db, error = get_database_connection()
            if error or client is None or db is None:
                print(f"Could not update database: {error}")
                return False

            # Store relative paths in database
            latest_version = {
                "source_file": to_project_relative(source_file),
                "published_path": to_project_relative(published_path),
                "selected_item": selected_item,
                "created_time": datetime.now(timezone.utc)
            }

            # Add the latest version to the document
            update_result = db["publishes"].update_one(
                {"_id": publish_document["_id"]},
                {
                    "$set": {
                        "published_versions.latest": latest_version,
                        "last_updated": datetime.now(timezone.utc)
                    }
                }
            )
            
            client.close()
            
            if update_result.modified_count > 0:
                print(f"✅ Latest version added to publish document")
                return True
            else:
                print(f"❌ Failed to update publish document")
                return False

        except Exception as e:
            print(f"Failed to add latest version: {e}")
            return False

    def update_publish_database(self, final_asset_name: str, publish_type: str, selected_item: str, published_path: str, source_file: str, custom_name: str):
        """Update database with publish information - legacy method for compatibility"""
        # Extract asset name from source file path
        source_path = Path(source_file)
        source_asset = source_path.parent.name
        
        # Get or create the publish document
        publish_document, _ = self.get_or_create_publish_document(source_asset, publish_type, custom_name)
        
        if publish_document:
            return self.add_latest_version_to_document(publish_document, selected_item, published_path, source_file)
        else:
            print(f"Failed to get/create publish document")
            return False