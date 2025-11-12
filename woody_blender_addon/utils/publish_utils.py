"""
Shared utilities for publish-related operations in the Woody Blender addon.
Contains common functions used across multiple operators.
"""

import bpy
from pathlib import Path
from .get_db_connection import get_database_connection


def to_project_relative(absolute_path: str) -> str:
    """
    Convert an absolute path to a project-relative path using project name from Blender prefs.
    
    Example:
        Input: "\\\\100.113.50.90\\projects\\PUD\\dev\\FlxAV_woody2Proj\\assets\\CnB\\cok\\aaa_latest.blend"
        Output: "assets\\CnB\\cok\\aaa_latest.blend"
    
    Args:
        absolute_path: Full absolute path string
        
    Returns:
        Project-relative path with backslashes, or original path if conversion fails
    """
    try:
        # Get project name from addon preferences
        addon_prefs = bpy.context.preferences.addons["woody_blender_addon"].preferences
        project_name = addon_prefs.project_name
        
        if not project_name:
            return absolute_path
        
        # Find the project name in the path and take everything after it
        path_str = str(absolute_path)
        
        # Look for the project name followed by a path separator
        project_markers = [
            f"\\{project_name}\\",
            f"/{project_name}/",
            f"\\{project_name}/",
            f"/{project_name}\\"
        ]
        
        for marker in project_markers:
            if marker in path_str:
                # Split at the marker and take everything after it
                parts = path_str.split(marker, 1)
                if len(parts) == 2:
                    relative_part = parts[1]
                    # Normalize to backslashes for consistency
                    return relative_part.replace('/', '\\')
        
        # If project name not found, return original path
        return absolute_path
        
    except Exception as e:
        print(f"Error converting to project relative path: {e}")
        return absolute_path

def to_absolute_path(project_relative_path: str) -> str:
    """
    Convert a project-relative path to an absolute path using database settings.
    
    Example:
        Input: "assets\\CnB\\cok\\aaa_latest.blend"
        Output (Windows): "\\\\100.113.50.90\\projects\\PUD\\dev\\FlxAV_woody2Proj\\assets\\CnB\\cok\\aaa_latest.blend"
        Output (Mac): "/Volumes/projects/PUD/dev/FlxAV_woody2Proj/assets/CnB/cok/aaa_latest.blend"
    
    Args:
        project_relative_path: Project-relative path string
        
    Returns:
        Absolute path for current OS, or original path if conversion fails
    """
    try:
        import platform
        from .get_db_connection import get_database_connection
        
        # Get database connection
        client, db, error = get_database_connection()
        if error or client is None or db is None:
            print(f"Database connection failed: {error}")
            return project_relative_path
        
        current_os = platform.system()
        
        # Get project settings from database
        settings = db["settings"].find_one({"project_name": {"$exists": True}})
        
        if not settings:
            print("No project settings found in database")
            client.close()
            return project_relative_path
        
        host_address = settings.get("host_address")
        location = settings.get("location", "")
        project_name = settings.get("project_name", "")
        
        client.close()
        
        if not all([host_address, location, project_name]):
            print(f"Missing required settings: host_address={host_address}, location={location}, project_name={project_name}")
            return project_relative_path
        
        # Build absolute path based on OS
        if current_os == "Darwin":
            # Mac: /Volumes/location/project_name/relative_path
            absolute_path = f"/Volumes/{location}/{project_name}/{project_relative_path}".replace('\\', '/')
        elif current_os == "Windows":
            # Windows: \\host_address\location\project_name\relative_path
            absolute_path = f"\\\\{host_address}\\{location}\\{project_name}\\{project_relative_path}"
        else:
            print(f"Warning: Unsupported OS: {current_os}, returning original path.")
            return project_relative_path
        
        return absolute_path
        
    except Exception as e:
        print(f"Error converting to absolute path: {e}")
        return project_relative_path

def get_override_status(library_path: str) -> str:
    """
    Check if any assets from this library are overridden AND actually used in the scene.
    
    Args:
        library_path: The file path of the library to check
        
    Returns:
        'overridden' if any assets are overridden and in scene, 'linked' otherwise
    """
    # Check collections - look for overrides that reference this library AND are in scene
    for col in bpy.data.collections:
        if col.override_library and col.override_library.reference:
            # Check if the reference collection is from our library
            ref = col.override_library.reference
            if ref.library and ref.library.filepath == library_path:
                # Only count if the overridden collection is actually in the scene
                if collection_in_scene(col):
                    return 'overridden'
        # Also check direct library matches with override_library set
        elif col.library and col.library.filepath == library_path and col.override_library:
            if collection_in_scene(col):
                return 'overridden'
    
    # Check objects - look for overrides that reference this library AND are in scene
    for obj in bpy.data.objects:
        if obj.override_library and obj.override_library.reference:
            # Check if the reference object is from our library
            ref = obj.override_library.reference
            if ref.library and ref.library.filepath == library_path:
                # Only count if the overridden object is actually in the scene
                if obj.name in bpy.context.scene.objects:
                    return 'overridden'
        # Also check direct library matches with override_library set
        elif obj.library and obj.library.filepath == library_path and obj.override_library:
            if obj.name in bpy.context.scene.objects:
                return 'overridden'
    
    # Check materials - look for overrides that reference this library
    # Show all linked materials since they may be used later
    for mat in bpy.data.materials:
        if mat.override_library and mat.override_library.reference:
            # Check if the reference material is from our library
            ref = mat.override_library.reference
            if ref.library and ref.library.filepath == library_path:
                return 'overridden'
        # Also check direct library matches with override_library set
        elif mat.library and mat.library.filepath == library_path and mat.override_library:
            return 'overridden'
    
    # Check meshes - look for overrides that reference this library AND are used in scene
    for mesh in bpy.data.meshes:
        if mesh.override_library and mesh.override_library.reference:
            # Check if the reference mesh is from our library
            ref = mesh.override_library.reference
            if ref.library and ref.library.filepath == library_path:
                # Only count if the overridden mesh is used by objects in the scene
                if _is_mesh_used_in_scene(mesh):
                    return 'overridden'
        # Also check direct library matches with override_library set
        elif mesh.library and mesh.library.filepath == library_path and mesh.override_library:
            if _is_mesh_used_in_scene(mesh):
                return 'overridden'
    
    # Check node groups - look for overrides that reference this library
    # Show all linked node groups since they may be used later
    for node_group in bpy.data.node_groups:
        if node_group.override_library and node_group.override_library.reference:
            # Check if the reference node group is from our library
            ref = node_group.override_library.reference
            if ref.library and ref.library.filepath == library_path:
                return 'overridden'
        # Also check direct library matches with override_library set
        elif node_group.library and node_group.library.filepath == library_path and node_group.override_library:
            return 'overridden'
    
    return 'linked'


def _is_material_used_in_scene(material) -> bool:
    """Helper function to check if a material is used by any object in the scene."""
    for obj in bpy.context.scene.objects:
        if obj.data and hasattr(obj.data, 'materials'):
            # Check materials using proper Blender API
            for mat_slot in obj.data.materials:
                if mat_slot == material:
                    return True
        if hasattr(obj, 'material_slots'):
            for slot in obj.material_slots:
                if slot.material == material:
                    return True
    return False


def _is_mesh_used_in_scene(mesh) -> bool:
    """Helper function to check if a mesh is used by any object in the scene."""
    for obj in bpy.context.scene.objects:
        if obj.data == mesh:
            return True
    return False


def _is_node_group_used_in_scene(node_group) -> bool:
    """Helper function to check if a node group is used in any material or modifier in the scene."""
    # Check if node group is used in any material used in the scene
    for material in bpy.data.materials:
        if material.use_nodes and material.node_tree:
            for node in material.node_tree.nodes:
                if hasattr(node, 'node_tree') and node.node_tree == node_group:
                    # Check if this material is used in the scene
                    if _is_material_used_in_scene(material):
                        return True
    
    # Check geometry node modifiers
    for obj in bpy.context.scene.objects:
        for modifier in obj.modifiers:
            if modifier.type == 'NODES' and modifier.node_group == node_group:
                return True
    
    return False


def get_display_name_from_db(library_path: str) -> str:
    """
    Get display name from database instead of parsing filename.
    
    Args:
        library_path: The file path of the library
        
    Returns:
        Formatted display name or filename as fallback
    """
    try:
        client, db, error = get_database_connection()
        if error or client is None or db is None:
            # Fallback to filename if DB is unavailable
            return bpy.path.basename(library_path)

        # Search through all publish documents
        for publish_doc in db["publishes"].find():
            published_versions = publish_doc.get("published_versions", {})
            
            # Check each version to see if it matches our library path
            for version, version_info in published_versions.items():
                if version_info.get("published_path") == library_path:
                    # Found a match! Build display name
                    publish_type = publish_doc.get("publish_type", "Unknown")
                    custom_name = publish_doc.get("custom_name", "Unknown")
                    
                    client.close()
                    return f"{publish_type.title()} - {custom_name} - {version}"
        
        client.close()
        # If not found in DB, fallback to filename
        return bpy.path.basename(library_path)
        
    except Exception as e:
        print(f"Error getting display name from DB: {e}")
        # Fallback to filename if error
        return bpy.path.basename(library_path)


def get_publish_type_from_db(library_path: str) -> str:
    """
    Get publish type from database for a given library path.
    
    Args:
        library_path: The file path of the library
        
    Returns:
        Publish type (e.g., 'MATERIAL', 'NODE_GROUP') or 'UNKNOWN' as fallback
    """
    try:
        client, db, error = get_database_connection()
        if error or client is None or db is None:
            return 'UNKNOWN'

        # Search through all publish documents
        for publish_doc in db["publishes"].find():
            published_versions = publish_doc.get("published_versions", {})
            
            # Check each version to see if it matches our library path
            for version, version_info in published_versions.items():
                if version_info.get("published_path") == library_path:
                    publish_type = publish_doc.get("publish_type", "UNKNOWN")
                    client.close()
                    return publish_type.upper()
        
        client.close()
        return 'UNKNOWN'
        
    except Exception as e:
        print(f"Error getting publish type from DB: {e}")
        return 'UNKNOWN'


def collection_in_scene(col, parent=None) -> bool:
    """
    Check if a collection is in the scene hierarchy (at any depth).
    
    Args:
        col: The collection to check
        parent: Parent collection to start search from (defaults to scene collection)
        
    Returns:
        True if collection is in scene, False otherwise
    """
    if parent is None:
        parent = bpy.context.scene.collection

    if col == parent:
        return True

    # Use proper Blender API to check children
    for child in parent.children:
        if child == col:
            return True
        if collection_in_scene(col, child):
            return True

    return False


def unlink_collection_from_scene(col, parent=None) -> bool:
    """
    Recursively unlink a collection from the scene hierarchy if present.
    
    Args:
        col: The collection to unlink
        parent: Parent collection to start search from (defaults to scene collection)
        
    Returns:
        True if collection was unlinked, False otherwise
    """
    if parent is None:
        parent = bpy.context.scene.collection

    # Check if collection is a direct child using proper comparison
    for child in parent.children:
        if child == col:
            parent.children.unlink(col)
            return True

    # Recursively check children
    for child in parent.children:
        if unlink_collection_from_scene(col, child):
            return True

    return False


def get_all_linked_libraries():
    """
    Get all linked library file paths from assets actually used in the current scene.
    
    Returns:
        Set of library file paths
    """
    linked_libraries = set()
    
    # Collections - only count those actually in the scene hierarchy
    for collection in bpy.data.collections:
        if collection.library and collection_in_scene(collection):
            linked_libraries.add(collection.library.filepath)
        elif collection.override_library and collection.override_library.reference:
            # Also check override collections that reference libraries
            ref = collection.override_library.reference
            if ref.library and collection_in_scene(collection):
                linked_libraries.add(ref.library.filepath)
    
    # Materials - show all linked materials (not just those in use)
    # Users explicitly load materials to use them later
    for material in bpy.data.materials:
        if material.library:
            linked_libraries.add(material.library.filepath)
    
    # Objects - only count those actually in the scene
    for obj in bpy.context.scene.objects:
        if obj.library:
            linked_libraries.add(obj.library.filepath)
        elif obj.override_library:
            # This is an override object - check if it references a library
            if obj.override_library.reference and obj.override_library.reference.library:
                linked_libraries.add(obj.override_library.reference.library.filepath)
    
    # Meshes - only count those used by objects in the scene
    for mesh in bpy.data.meshes:
        if mesh.library:
            # Check if mesh is used by any object in the scene
            mesh_used = False
            for obj in bpy.context.scene.objects:
                if obj.data == mesh:
                    mesh_used = True
                    break
            if mesh_used:
                linked_libraries.add(mesh.library.filepath)
    
    # Node groups - show all linked node groups (not just those in use)
    # Users explicitly load node groups to use them later
    for node_group in bpy.data.node_groups:
        if node_group.library:
            linked_libraries.add(node_group.library.filepath)

    return linked_libraries


def refresh_loaded_publishes_data(context):
    """
    Refresh the scene properties with current loaded publishes data.
    
    Args:
        context: Blender context
    """
    loaded_publishes = []
    linked_libraries = get_all_linked_libraries()
    
    # Get display info from database for each library
    for library_path in linked_libraries:
        display_name = get_display_name_from_db(library_path)
        override_status = get_override_status(library_path)
        publish_type = get_publish_type_from_db(library_path)
        
        loaded_publishes.append({
            'library_path': library_path,
            'display_name': display_name,
            'override_status': override_status,
            'publish_type': publish_type
        })
    
    # Store in scene for display
    context.scene.woody_loaded_publishes_count = len(loaded_publishes)
    
    # Create formatted display strings for UI (now includes override status)
    display_strings = []
    for pub in loaded_publishes:
        status_icon = "🔒" if pub['override_status'] == 'overridden' else "🔗"
        display_strings.append(f"{status_icon} {pub['display_name']}")
    
    context.scene.woody_loaded_publishes_display = "\n".join(display_strings) if display_strings else "No published assets loaded"
    
    # Store the publish data for UI buttons
    import json
    context.scene.woody_loaded_publishes_data = json.dumps(loaded_publishes)