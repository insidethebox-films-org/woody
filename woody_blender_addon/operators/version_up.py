import bpy
import os
import re
import shutil

from pathlib import Path
from ..utils.get_db_connection import get_database_connection
from ..utils.publish_utils import to_project_relative

class WOODY_OT_version_up(bpy.types.Operator):
    bl_idname = "woody.version_up"
    bl_label = "Version Up"
    bl_description = "Save current scene and create a new version"
    
    def execute(self, context):
        try:
            # Check if scene has been saved
            if not bpy.data.filepath:
                self.report({'ERROR'}, "Scene has not been saved before. Save it first.")
                return {'CANCELLED'}
            
            # Save current scene first
            bpy.ops.wm.save_mainfile()
            
            # Get current file info
            current_path = Path(bpy.data.filepath)
            directory = current_path.parent
            extension = current_path.suffix
            filename = current_path.stem
            
            # Check if current file is already a versioned file (e.g., aaa_v9.blend)
            version_check_pattern = re.compile(r".*_v\d+$")
            if version_check_pattern.match(filename):
                self.report({'ERROR'}, "Cannot version up from a versioned file. Open the _latest file instead.")
                return {'CANCELLED'}
            
            # Remove _latest suffix if it exists
            base_filename = filename.replace("_latest", "")
            
            print(f"Processing file: {base_filename}")
            
            # Find existing versions
            version_pattern = re.compile(rf"{re.escape(base_filename)}_v(\d+){re.escape(extension)}$")
            existing_versions = []
            
            for file in directory.iterdir():
                if file.is_file():
                    match = version_pattern.match(file.name)
                    if match:
                        existing_versions.append(int(match.group(1)))
            
            # Calculate next version
            next_version = max(existing_versions, default=0) + 1
            new_filename = f"{base_filename}_v{next_version}{extension}"
            new_file_path = directory / new_filename
            
            # Copy current file to new version
            shutil.copy2(current_path, new_file_path)

            # Create the new _latest filename
            new_latest_filename = f"{base_filename}_latest{extension}"
            new_latest_path = directory / new_latest_filename
            
            # Save current scene as _latest (this will rename the current file)
            bpy.ops.wm.save_as_mainfile(filepath=str(new_latest_path))

            # Remove the original file if it's different from the new _latest file
            if current_path != new_latest_path and current_path.exists():
                os.remove(current_path)
                # Remove Blender's automatic backup file (.blend1)
                backup_file = current_path.with_suffix(current_path.suffix + '1')
                if backup_file.exists():
                    os.remove(backup_file)
            
            # Update database with new version info (using relative paths)
            self.update_database(base_filename, str(new_file_path), str(new_latest_path), next_version)
            
            print(f"Created version: {new_file_path}")
            print(f"Working file: {new_latest_path}")
            self.report({'INFO'}, f"Version {next_version} created successfully")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Version up failed: {str(e)}")
            return {'CANCELLED'}
        
    def update_database(self, blend_name: str, version_path: str, latest_path: str, version_number: int):
        """Update database with new version information"""
        try:
            from datetime import datetime, timezone
            
            # Get database connection using the utility function
            client, db, error = get_database_connection()
            
            if error:
                print(f"Database connection failed: {error}")
                self.report({'WARNING'}, f"Database update failed: {error}")
                return
            
            if client is None or db is None:
                print("Could not establish database connection")
                self.report({'WARNING'}, "Could not connect to database")
                return
            
            # Get addon preferences for logging
            addon_prefs = bpy.context.preferences.addons["woody_blender_addon"].preferences
            print(f"Connecting to database: {addon_prefs.project_name} at {addon_prefs.mongodb_address}")
            
            # Find the blend document - try both base name and with _latest suffix
            collection = db["blends"]
            blend_doc = collection.find_one({"name": blend_name})
            
            if not blend_doc:
                # Try with _latest suffix (for existing documents)
                blend_name_with_latest = f"{blend_name}_latest"
                blend_doc = collection.find_one({"name": blend_name_with_latest})
                print(f"DEBUG - Tried searching with: '{blend_name_with_latest}'")
            
            if not blend_doc:
                print(f"Warning: Blend document '{blend_name}' or '{blend_name}_latest' not found in database")
                print("Skipping database update - blend document must be created through the main Woody application first")
                client.close()
                return
            
            print(f"✓ Found blend document: {blend_doc.get('name')}")
            
            # Get existing blend_files or create new dict
            blend_files = blend_doc.get("blend_files", {})
            
            # Remove old latest path if it exists and is different
            old_latest_key = None
            for key, value in blend_files.items():
                if value == "latest" and key != to_project_relative(latest_path):
                    old_latest_key = key
                    break

            if old_latest_key:
                print(f"DEBUG - Removing old latest key: {old_latest_key}")

            # Update blend_files dictionary (convert to relative paths)
            relative_version_path = to_project_relative(version_path)
            relative_latest_path = to_project_relative(latest_path)
            blend_files[relative_version_path] = version_number
            blend_files[relative_latest_path] = "latest"
            
            # Remove old latest if found
            if old_latest_key:
                blend_files.pop(old_latest_key, None)
                    
            print(f"DEBUG - Updating blend_files with: {len(blend_files)} entries")
            
            # Update the document with the complete blend_files object
            update_data = {
                "$set": {
                    "blend_files": blend_files,
                    "modified_time": datetime.now(timezone.utc),
                    "latest_version": version_number
                }
            }
            
            # Update the document
            result = collection.update_one(
                {"_id": blend_doc["_id"]},
                update_data
            )
            
            if result.modified_count > 0:
                print(f"✓ Database updated successfully for blend '{blend_doc.get('name')}' - Version {version_number}")
                print(f"  - Added version: {relative_version_path} = {version_number}")
                print(f"  - Updated latest: {relative_latest_path} = 'latest'")
                if old_latest_key:
                    print(f"  - Removed old latest: {old_latest_key}")
                
                self.report({'INFO'}, f"Database updated - Version {version_number}")
            else:
                print(f"⚠ No changes made to database for blend '{blend_doc.get('name')}'")
                self.report({'WARNING'}, "No database changes made")
            
            # Close connection
            client.close()
            print("✓ Database connection closed")
            
        except ImportError as e:
            error_msg = f"Database update failed - missing library: {str(e)}"
            print(error_msg)
            print("Make sure pymongo is installed in Blender's Python environment")
            self.report({'ERROR'}, "Missing required libraries")
        except Exception as e:
            error_msg = f"Database update failed: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Database error: {str(e)}")
        