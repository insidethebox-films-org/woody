"""
Load Publish Operator for the Woody Blender addon.
Handles loading published assets using publish ID and version.
"""

import bpy
import platform
from pathlib import Path
from ...utils.get_db_connection import get_database_connection
from ...utils.asset_loaders import load_by_type
from ...utils.publish_utils import refresh_loaded_publishes_data
from ...utils.publish_utils import to_absolute_path


class WOODY_OT_load_publish(bpy.types.Operator):
    bl_idname = "woody.load_publish"
    bl_label = "Load Publish"
    bl_description = "Link a published asset using publish ID and version"

    def execute(self, context):
        # Get the clipboard-style input from scene property
        raw_input = getattr(context.scene, 'woody_publish_id', '').strip()
        
        if not raw_input:
            self.report({'ERROR'}, "Please paste a publish ID in format: id#ver:version")
            return {'CANCELLED'}
        
        # Parse clipboard format: <publish_id>#ver:<version>
        if '#ver:' not in raw_input:
            self.report({'ERROR'}, "Invalid format. Expected: id#ver:version")
            return {'CANCELLED'}
        
        try:
            publish_id, version = raw_input.split('#ver:', 1)
            publish_id = publish_id.strip()
            version = version.strip()
            
            if not publish_id or not version:
                self.report({'ERROR'}, "Invalid format. Both ID and version are required")
                return {'CANCELLED'}
                
        except Exception:
            self.report({'ERROR'}, "Failed to parse input. Expected format: id#ver:version")
            return {'CANCELLED'}

        # Query database for publish information
        publish_info = self.get_publish_info(publish_id, version)
        if not publish_info:
            self.report({'ERROR'}, f"Could not find publish with ID: {publish_id}, version: {version}")
            return {'CANCELLED'}
        
        # Extract file path and metadata
        blend_path = Path(publish_info['file_path']).resolve()
        publish_type = publish_info['publish_type']
        custom_name = publish_info['custom_name']
        
        if not blend_path.exists():
            self.report({'ERROR'}, f"Published file not found: {blend_path}")
            return {'CANCELLED'}

        # Prevent linking from the current file
        current_path = Path(bpy.data.filepath).resolve() if bpy.data.filepath else None
        if current_path and current_path == blend_path:
            self.report({'ERROR'}, "Cannot link from the current file")
            return {'CANCELLED'}

        try:
            # Load based on publish type
            linked_items = load_by_type(str(blend_path), publish_type, context)
            
            if linked_items:
                items_str = ", ".join(linked_items)
                display_name = f"{publish_type.title()} - {custom_name} - {version}"
                self.report({'INFO'}, f"✅ Linked {publish_type}: {items_str}")
                
                # Clear the input field after successful load
                context.scene.woody_publish_id = ""
                
                # Refresh the loaded publishes list
                refresh_loaded_publishes_data(context)
                
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, f"Failed to link any {publish_type}s")
                return {'CANCELLED'}

        except Exception as e:
            self.report({'ERROR'}, f"Loading failed: {str(e)}")
            return {'CANCELLED'}

    def get_publish_info(self, publish_id: str, version: str):
        """Query database for publish information"""
        try:
            client, db, error = get_database_connection()
            if error or client is None or db is None:
                print(f"Database connection error: {error}")
                return None

            # Find the publish document by ID
            publish_doc = db["publishes"].find_one({"publish_id": publish_id})
            
            if not publish_doc:
                client.close()
                return None
            
            # Get the specific version
            published_versions = publish_doc.get("published_versions", {})
            
            if version not in published_versions:
                client.close()
                return None
            
            version_info = published_versions[version]
            
            # Return combined information
            result = {
                "file_path": to_absolute_path(version_info.get("published_path", "")),
                "publish_type": publish_doc.get("publish_type", ""),
                "custom_name": publish_doc.get("custom_name", ""),
                "source_asset": publish_doc.get("source_asset", ""),
                "version": version,
                "publish_id": publish_id
            }

            client.close()
            return result
            
        except Exception as e:
            print(f"Error querying publish info: {e}")
            return None