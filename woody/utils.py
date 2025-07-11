import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

from .preferences import *

def publish(collection_name, tags): # DEPRECATED
    # Make sure there is a valid active collection
    active_collection = bpy.context.view_layer.active_layer_collection.collection

    if not active_collection:
        print("❌ Error: No collection selected.")
        return
    
    # Rename the collection to the new name
    active_collection.name = collection_name
    print(f"✅ Renamed collection to: {collection_name}")

    # Handle the asset data
    asset_data = active_collection.asset_data
    if asset_data:
        for tag in tags:
            # Check if the tag already exists
            if tag not in asset_data.tags:
                # Only add the tag if it's not already present
                asset_data.tags.new(tag)
                print(f"Added tag: {tag}")
            else:
                print(f"Tag '{tag}' already exists, skipping.")
    else:
        print("❌ Error: Could not access asset data.")

    # Generate preview for the asset (requires an active object)
    obj = bpy.context.object
    if obj is None:
        print("❌ Error: No object selected.")
        return
    
    if not obj.asset_data:
        print(f"❌ Error: Object '{obj.name}' is not marked as an asset.")
        return

    try:
        bpy.ops.ed.lib_id_generate_preview({'area': bpy.context.area}, id=obj)
        print(f"✅ Generated preview for asset: {obj.name}")
    except RuntimeError as e:
        print(f"❌ Failed to generate preview: {e}")

def create_blend_with_collection(file_name, collection_name, target_directory): # DEPRECATED

    blender_exe = get_blender_version()

    # Ensure the target directory exists
    target_dir = Path(target_directory)
    os.makedirs(target_dir, exist_ok=True)

    file_path = target_dir / file_name
    file_path_str = str(file_path)  # Convert to string for subprocess

    if file_path.exists():
        print(f"✅ Blend file already exists: {file_path}. Skipping creation.")
        return

    # Ensure no spaces or special characters cause issues
    file_path_str = file_path_str.replace("\\", "\\\\")

    blender_command = [
        blender_exe, "--background", "--python-expr",
        (
            "import bpy; "
            "bpy.ops.wm.read_homefile(use_empty=True); "  # Load user preferences WITHOUT default objects
            "bpy.ops.object.select_all(action='SELECT'); "  # Select all objects
            "bpy.ops.object.delete(); "  # Delete all objects (removes cube, camera, light)
            f"new_collection = bpy.data.collections.new('{collection_name}'); "  # Create collection
            "bpy.context.scene.collection.children.link(new_collection); "  # Link collection
            "bpy.context.view_layer.update(); "  # Ensure scene updates before saving
            f"bpy.ops.wm.save_as_mainfile(filepath=r'{file_path_str}'); "  # Save file
            f"print('✅ Successfully created: {file_path_str}');"
        )
    ]

    # Run the command to create a new Blender instance and execute the code
    result = subprocess.run(blender_command, capture_output=True, text=True)
    
    # Debugging output: print any result or errors from Blender
    print(result.stdout)
    print(result.stderr)

    # Check if the file has been successfully created
    if os.path.exists(file_path):
        print(f"✅ Successfully created the .blend file at: {file_path}")
    else:
        print(f"❌ Error: The .blend file was not created at {file_path}")

def create_blend_with_collection_FV(file_name, collection_name, target_directory): 
    from pathlib import Path
    import bpy
    import os

    # Ensure the target directory exists
    target_dir = Path(target_directory)
    os.makedirs(target_dir, exist_ok=True)

    file_path = target_dir / file_name
    file_path_str = str(file_path)

    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"❌ Collection '{collection_name}' not found in current file.")
        return

    # Get all objects inside the collection
    #objects = {obj for obj in collection.all_objects}

    # Optionally gather mesh, materials, etc.
   # meshes = {obj.data for obj in objects if obj.type == 'MESH' and obj.data}
    #materials = {mat for obj in objects if obj.type == 'MESH' for mat in obj.data.materials if mat}
    
    datablocks = {collection} #| objects | meshes | materials

    try:
        bpy.data.libraries.write(
            file_path_str,
            datablocks,
            fake_user=True,
            compress=True
        )
        #print(f"✅ Exported: '{collection_name}' with {len(objects)} object(s), {len(meshes)} mesh(es), {len(materials)} material(s)")
    except Exception as e:
        print(f"❌ Failed to export collection: {e}")

def open_publish_blend_file(file_path):

    blender_exe = get_blender_version()

    if not os.path.exists(file_path):
        print(f"❌ Error: File does not exist - {file_path}")
        return

    subprocess.Popen([blender_exe, file_path], close_fds=True, start_new_session=True)

    print(f"✅ Opened Blender in a separate instance with file: {file_path}")

def select_objects_in_selected_collection(collection_name): # DEPRECATED

    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    
    # Find the collection by name
    collection = bpy.data.collections.get(collection_name)
    
    if not collection:
        print(f"❌ Error: Collection with name '{collection_name}' not found.")
        return

    # Select all objects in the collection
    for obj in collection.objects:
        obj.select_set(True)

    # Output the result
    print(f"✅ Selected all objects in the collection: {collection_name}")

def export_selection_to_usd(export_path, export_format='USD'): # DEPRECATED

    if not bpy.context.selected_objects:
        print("❌ Error: No objects selected for export.")
        return

    os.makedirs(os.path.dirname(export_path), exist_ok=True)

    bpy.ops.wm.usd_export(
                    filepath=export_path, 
                    check_existing=False, 
                    selected_objects_only=True, 
                    visible_objects_only=True, 
                    export_animation=True, 
                    export_hair=True, 
                    export_uvmaps=True, 
                    export_mesh_colors=True, 
                    export_normals=True, 
                    export_materials=True, 
                    export_subdivision='BEST_MATCH', 
                    export_armatures=True, 
                    use_instancing=True, 
                    relative_paths=True, 
                    root_prim_path='/root', 
                    convert_world_material=True, 
                    export_meshes=True, 
                    export_lights=True, 
                    export_cameras=True, 
                    export_curves=True, 
                    export_volumes=True,
                    )

    print(f"✅ Successfully exported selection to: {export_path}")

def create_publish_workspace(workspace_name="My Custom Workspace"): # DEPRECATED

    if workspace_name in bpy.data.workspaces:
        workspace = bpy.data.workspaces[workspace_name]
    else:
        workspace = bpy.data.workspaces.new(name=workspace_name)

    # Set the workspace as active
    bpy.context.window.workspace = workspace

    # Get the screen layout (use the first screen)
    screen = workspace.screens[0]

    # Define initial layout with File Browser
    areas_setup = [
        ("VIEW_3D", 0, 0, 0.25, 1), 
        ("OUTLINER", 0, 0.5, 0.25, 0.5), 
        ("FILE_BROWSER", 1, 0, 0.75, 1)  # Start with File Browser
    ]

    # Assign editor types to existing areas
    for i, (editor_type, x, y, width, height) in enumerate(areas_setup):
        area = screen.areas[i]  # Use existing areas
        area.type = editor_type  # Set the editor type

    # Function to switch File Browser to Asset Browser
    def switch_to_asset_browser():
        for area in screen.areas:
            if area.type == "FILE_BROWSER":
                area.ui_type = "ASSETS"  # Change UI to Asset Browser

                # Ensure params are accessible
                params = area.spaces.active.params
                if params:
                    try:
                        params.asset_library_ref = 'Assets Library'  # Custom Library Name
                    except TypeError:
                        params.asset_library_ref = 'LOCAL'  # Fallback

                    params.import_type = 'APPEND'  # Set to Append Mode
                    print("✅ Switched File Browser to Asset Browser!")
                return  # Exit loop after changing first match

    # Register a timer to ensure UI update happens after Blender refresh
    bpy.app.timers.register(switch_to_asset_browser)

    print(f"✅ Workspace '{workspace_name}' created successfully!")

def rename_workspace(old_name, new_name): # DEPRECATED

    if old_name in bpy.data.workspaces:
        bpy.data.workspaces[old_name].name = new_name
        print(f"✅ Workspace renamed from '{old_name}' to '{new_name}'")
    else:
        print(f"✅ Workspace '{old_name}' not found!")

def delete_collection_contents(collection_name): # DEPRECATED

    # Get the collection
    collection = bpy.data.collections.get(collection_name)

    if not collection:
        print(f"❌ Collection '{collection_name}' not found.")
        return
    
    # Delete all objects in the collection
    for obj in list(collection.objects):  # Convert to list to avoid iteration issues
        bpy.data.objects.remove(obj, do_unlink=True)  # Remove from Blender

    print(f"✅ Deleted all objects in collection '{collection_name}'.")

    # Clean up orphan data (meshes, materials, etc.)
    for data_type in ('meshes', 'materials', 'textures', 'images', 'curves', 'grease_pencils'):
        for data in getattr(bpy.data, data_type):
            if not data.users:  # If no users exist, remove it
                getattr(bpy.data, data_type).remove(data)

    print("✅ Cleaned up orphan data.")

def import_usdc_to_collection(file_path, collection_name): # DEPRECATED

    # Ensure the file exists
    if not os.path.isfile(file_path):
        print(f"❌ USD file not found: {file_path}")
        return
    
    # Ensure the collection exists, create it if not
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)

    # Import the USD file
    bpy.ops.wm.usd_import(filepath=file_path)

    # Get all newly imported objects
    imported_objects = [obj for obj in bpy.context.selected_objects]

    # Move imported objects to the target collection
    for obj in imported_objects:
        # Unlink from the default collection
        for col in obj.users_collection:
            col.objects.unlink(obj)
        
        # Link to the specified collection
        collection.objects.link(obj)

    print(f"✅ Imported '{os.path.basename(file_path)}' into collection '{collection_name}'.")
