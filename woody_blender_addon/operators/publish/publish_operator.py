import bpy
from pathlib import Path

from .element_gatherers import ElementGatherer
from .db_handler import PublishDatabaseHandler
from ...utils.publish_utils import to_project_relative

def on_publish_type_changed(self, context):
    """Called when publish type changes - refresh the existing names"""
    try:
        # Clear existing names to force refresh - use string identifier instead of int
        self.existing_names = "NONE"
        # Also clear the custom name when type changes
        self.custom_name = ""
    except:
        pass

def on_custom_name_changed(self, context):
    """Called when user types in custom_name - update filtered suggestions"""
    # This will trigger the enum callback to refresh with filtered results
    pass

def on_suggestion_selected(self, context):
    """Called when user selects a suggestion from the dropdown"""
    if hasattr(self, 'name_suggestions'):
        selected = self.name_suggestions
        
        if selected not in ["NONE", "ERROR"]:
            self.custom_name = selected

def get_filtered_suggestions_callback(self, context):
    """Get suggestions filtered by current custom_name input"""
    try:
        # Get current asset name from path
        current_file = Path(bpy.data.filepath)
        if not current_file.name:
            return [("NONE", "Save file first", "Save your blend file to see suggestions")]
        
        asset_name = current_file.parent.name  # e.g., "cok"
        
        # Check if publish_type exists on this instance
        if not hasattr(self, 'publish_type') or not self.publish_type:
            return [("NONE", "No type selected", "Select a publish type first")]
        
        # Get existing publishes from database
        db_handler = PublishDatabaseHandler()
        existing_names = db_handler.get_existing_names_for_type(asset_name, self.publish_type)
        
        # Get the current input text (what user has typed so far)
        current_input = getattr(self, 'custom_name', '').lower().strip()
        
        # Filter existing names based on user input
        filtered_names = []
        if current_input and existing_names:
            for name in existing_names:
                if current_input in name.lower():
                    filtered_names.append(name)
        
        # Build the items list
        items = []
        
        # If there are filtered matches, show them
        if filtered_names:
            for name in filtered_names:
                items.append((name, name, f"Existing: {name}"))
        
        # Always add an option for "no selection" if no matches or empty input
        if not filtered_names or not current_input:
            items.insert(0, ("NONE", "Type to search...", "Start typing to see matching names"))
        
        return items if items else [("NONE", "No matches", "No existing names match your input")]
        
    except Exception as e:
        print(f"Error getting filtered suggestions: {e}")
        return [("ERROR", "Error loading", f"Error: {str(e)}")]

def get_existing_names_callback(self, context):
    """External callback for existing names enum"""
    try:
        # Get current asset name from path
        current_file = Path(bpy.data.filepath)
        if not current_file.name:
            return [("NONE", "Save file first", "Save your blend file to see suggestions")]
        
        asset_name = current_file.parent.name  # e.g., "cok"
        
        # Check if publish_type exists on this instance
        if not hasattr(self, 'publish_type') or not self.publish_type:
            return [("NONE", "No type selected", "Select a publish type first")]
        
        # Get existing publishes from database
        db_handler = PublishDatabaseHandler()
        existing_names = db_handler.get_existing_names_for_type(asset_name, self.publish_type)
        
        # Always return at least one item to prevent the enum warning
        items = [("NONE", "Enter new name", "Create a new name")]
        
        # Add existing names if found
        if existing_names:
            for name in existing_names:
                items.append((name, name, f"Use existing name: {name}"))
        
        return items
        
    except Exception as e:
        print(f"Error getting existing names: {e}")
        # Always return a valid enum item to prevent warnings
        return [("ERROR", "Error loading", f"Error: {str(e)}")]

class WOODY_OT_publish(bpy.types.Operator):
    bl_idname = "woody.publish"
    bl_label = "Publish Asset"
    bl_description = "Publish selected asset as a reusable component"

    custom_name: bpy.props.StringProperty(
        name="Publish Name",
        description="Name for this specific publish - start typing to see suggestions",
        default="",
        update=on_custom_name_changed
    )#type: ignore

    asset_name: bpy.props.StringProperty(
        name="Asset Name",
        description="Name for the published asset/shot",
        default=""
    )#type: ignore
    
    publish_type: bpy.props.EnumProperty(
        name="Publish Type",
        description="What type of asset to publish",
        items=[
            ('COLLECTION', 'Collection', 'Publish entire collection with objects'),
            ('MATERIAL', 'Material Only', 'Publish material/shader only'),
            ('NODE_GROUP', 'Node Group', 'Publish node group (geometry or shader)'),
            ('OBJECT', 'Single Object', 'Publish individual object'),
            #('MESH', 'Mesh Only', 'Publish mesh geometry only'),
        ],
        default='COLLECTION',
        update=on_publish_type_changed
    )#type: ignore
    
    # Filtered suggestions that update as user types
    name_suggestions: bpy.props.EnumProperty(
        name="Suggestions",
        description="Matching existing names - select to use",
        items=get_filtered_suggestions_callback,
        update=on_suggestion_selected
    )#type: ignore
    
    # Legacy property - keeping for backward compatibility but hidden in UI
    existing_names: bpy.props.EnumProperty(
        name="Existing Names",
        description="Previously used names for this type",
        items=get_existing_names_callback
    )#type: ignore

    # Dynamic selection properties - these call ElementGatherer methods directly
    collection_name: bpy.props.EnumProperty(
        name="Collection",
        description="Select collection to publish",
        items=lambda self, context: ElementGatherer().get_collections_list()  # Direct call
    )#type: ignore
    
    material_name: bpy.props.EnumProperty(
        name="Material",
        description="Select material to publish",
        items=lambda self, context: ElementGatherer().get_materials_list()  # Direct call
    )#type: ignore
    
    mesh_name: bpy.props.EnumProperty(
        name="Mesh",
        description="Select mesh to publish",
        items=lambda self, context: ElementGatherer().get_meshes_list()  # Direct call
    )#type: ignore
    
    node_group_name: bpy.props.EnumProperty(
        name="Node Group",
        description="Select node group to publish",
        items=lambda self, context: ElementGatherer().get_node_groups_list()  # Direct call
    )#type: ignore
    
    object_name: bpy.props.EnumProperty(
        name="Object",
        description="Select object to publish",
        items=lambda self, context: ElementGatherer().get_objects_list()  # Direct call
    )#type: ignore

    def __init__(self):
        super().__init__()
        self.element_gatherer = ElementGatherer()
        self.db_handler = PublishDatabaseHandler()
    
    def get_final_asset_name(self):
        """Generate the final asset name following the pattern"""
        current_file = Path(bpy.data.filepath)
        if not current_file.name:
            return "unknown_asset"
        
        asset_name = current_file.parent.name  # e.g., "cok"
        user_name = self.custom_name.strip() or "unnamed"
        
        # Pattern: cok_COLLECTION_shower_publish_latest
        return f"{asset_name}_{self.publish_type}_{user_name}_publish_latest"
        
    def invoke(self, context, event):
        # Clear all fields for fresh start
        self.custom_name = ""
        self.existing_names = "NONE"
        self.name_suggestions = "NONE"
        return context.window_manager.invoke_props_dialog(self, width=500)

    def draw(self, context):
        layout = self.layout
        
        # Show the publish type first
        layout.prop(self, "publish_type")
        
        # Name input section
        layout.separator()
        layout.label(text="Publish Name:")
        
        # Main name input field
        layout.prop(self, "custom_name", text="")
        
        # Show suggestions if user has typed something and there are matches
        if self.custom_name.strip():
            # Get suggestions to check if there are any matches
            try:
                suggestions = get_filtered_suggestions_callback(self, context)
                # Only show suggestions if there are actual matches (not just "NONE" or "No matches")
                has_matches = False
                for item in suggestions:
                    if item[0] not in ["NONE", "ERROR"] and "No matches" not in item[1]:
                        has_matches = True
                        break
                
                if has_matches:
                    layout.separator()
                    row = layout.row()
                    row.label(text="Suggestions:", icon='DOWNARROW_HLT')
                    layout.prop(self, "name_suggestions", text="")
            except:
                pass  # Ignore errors in suggestion display
        
        # Show preview of final name
        if self.custom_name.strip():
            final_name = self.get_final_asset_name()
            layout.separator()
            box = layout.box()
            box.label(text=f"Final: {final_name}.blend", icon='FILE_BLEND')
        
        # Show what to publish based on type
        layout.separator()
        layout.label(text=f"Select {self.publish_type.title()} to Publish:")
        if self.publish_type == 'COLLECTION':
            layout.prop(self, "collection_name")
        elif self.publish_type == 'MATERIAL':
            layout.prop(self, "material_name")
        elif self.publish_type == 'MESH':
            layout.prop(self, "mesh_name")
        elif self.publish_type == 'NODE_GROUP':
            layout.prop(self, "node_group_name")
        elif self.publish_type == 'OBJECT':
            layout.prop(self, "object_name")

    def create_versioned_source_file(self, current_path):
        """Create a versioned copy of the current file for permanent source reference"""
        try:
            import os
            import re
            import shutil
            from datetime import datetime, timezone
            
            directory = current_path.parent
            extension = current_path.suffix
            filename = current_path.stem
            
            # Remove _latest suffix if it exists
            base_filename = filename.replace("_latest", "")
            
            print(f"Creating versioned source for: {base_filename}")
            
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
            versioned_path = directory / new_filename
            
            # Copy current file to versioned file
            shutil.copy2(current_path, versioned_path)
            
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
            
            # Update the blend database with version info (reuse version_up logic)
            self.update_blend_database(base_filename, str(versioned_path), str(new_latest_path), next_version)
            
            print(f"Created versioned source: {versioned_path}")
            return str(versioned_path)
            
        except Exception as e:
            print(f"Error creating versioned source: {e}")
            return None
    
    def update_blend_database(self, blend_name: str, version_path: str, latest_path: str, version_number: int):
        """Update blend database with new version information (adapted from version_up.py)"""
        try:
            from datetime import datetime, timezone
            from ...utils.get_db_connection import get_database_connection
            
            # Get database connection
            client, db, error = get_database_connection()
            
            if error or client is None or db is None:
                print(f"Database connection failed: {error}")
                return
            
            # Find the blend document
            collection = db["blends"]
            blend_doc = collection.find_one({"name": blend_name})
            
            if not blend_doc:
                # Try with _latest suffix
                blend_name_with_latest = f"{blend_name}_latest"
                blend_doc = collection.find_one({"name": blend_name_with_latest})
            
            if not blend_doc:
                print(f"Warning: Blend document '{blend_name}' not found in database")
                client.close()
                return
            
            # Get existing blend_files or create new dict
            blend_files = blend_doc.get("blend_files", {})
            
            # Remove old latest path if it exists and is different
            old_latest_key = None
            for key, value in blend_files.items():
                if value == "latest" and key != to_project_relative(latest_path):
                    old_latest_key = key
                    break

            # Update blend_files dictionary (convert to relative paths)
            relative_version_path = to_project_relative(version_path)
            relative_latest_path = to_project_relative(latest_path)
            blend_files[relative_version_path] = version_number
            blend_files[relative_latest_path] = "latest"
            
            # Remove old latest if found
            if old_latest_key:
                blend_files.pop(old_latest_key, None)
            
            # Update the document
            update_data = {
                "$set": {
                    "blend_files": blend_files,
                    "modified_time": datetime.now(timezone.utc),
                    "latest_version": version_number
                }
            }
            
            result = collection.update_one({"_id": blend_doc["_id"]}, update_data)
            
            if result.modified_count > 0:
                print(f"✓ Blend database updated - Version {version_number}")
            
            client.close()
            
        except Exception as e:
            print(f"Blend database update failed: {e}")

    def execute(self, context):
        try:
            current_path = Path(bpy.data.filepath)
            if not current_path.exists():
                self.report({'ERROR'}, "Save your blend file first!")
                return {'CANCELLED'}
            
            if not self.custom_name.strip():
                self.report({'ERROR'}, "Please enter a name for the asset!")
                return {'CANCELLED'}

            # Save the current file before publishing
            print("Saving current file before publishing...")
            bpy.ops.wm.save_mainfile()
            self.report({'INFO'}, "File saved before publishing")
            
            # Version up the working file to create a permanent source reference
            versioned_source_path = self.create_versioned_source_file(current_path)
            if not versioned_source_path:
                self.report({'ERROR'}, "Failed to create versioned source file")
                return {'CANCELLED'}
            
            print(f"Created versioned source: {versioned_source_path}")
            self.report({'INFO'}, f"Source versioned for permanent reference")

            # Create publish directory structure
            publish_dir = current_path.parent / "_publish"
            publish_dir.mkdir(exist_ok=True)
            
            # Get asset name for versioning logic
            source_asset = current_path.parent.name
            
            # Get or create the publish document for this asset+type+name combination
            publish_document, _ = self.db_handler.get_or_create_publish_document(
                source_asset, self.publish_type, self.custom_name
            )
            
            next_version = None
            if publish_document and "published_versions" in publish_document:
                published_versions = publish_document["published_versions"]
                
                # Check if 'latest' already exists
                if "latest" in published_versions:
                    # Get the next version number
                    next_version = self.db_handler.get_next_version_number(publish_document)
                    
                    # Move the existing 'latest' to a versioned entry
                    success, old_versioned_path = self.db_handler.version_latest_publish(
                        publish_document, next_version
                    )
                    
                    if success:
                        self.report({'INFO'}, f"Previous version archived as v{next_version}")
                        print(f"Existing publish archived as version {next_version}")
                    else:
                        self.report({'WARNING'}, "Failed to archive previous version, continuing...")
            
            # Create the published blend file with new naming pattern (always '_latest')
            final_asset_name = self.get_final_asset_name()
            published_file = publish_dir / f"{final_asset_name}.blend"
            
            # Use element gatherer for asset creation
            success = self.element_gatherer.create_published_asset(
                self.publish_type, 
                self.get_selected_item_name(),
                published_file
            )
            
            if success:
                # Add the new version as 'latest' to the document using versioned source
                db_success = self.db_handler.add_latest_version_to_document(
                    publish_document,
                    self.get_selected_item_name(),
                    str(published_file),
                    versioned_source_path
                )
                
                if db_success:
                    version_info = f" (previous archived as v{next_version})" if next_version else " (new)"
                    self.report({'INFO'}, f"✅ Published: {final_asset_name}{version_info}")
                    return {'FINISHED'}
                else:
                    self.report({'ERROR'}, "Failed to update database")
                    return {'CANCELLED'}
            else:
                self.report({'ERROR'}, "Failed to create published asset")
                return {'CANCELLED'}
                
        except Exception as e:
            self.report({'ERROR'}, f"Publish failed: {str(e)}")
            return {'CANCELLED'}

    def get_selected_item_name(self):
        """Get the selected item name based on publish type"""
        return getattr(self, f"{self.publish_type.lower()}_name")