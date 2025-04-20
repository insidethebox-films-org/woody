bl_info = {
    "name": "Woody",
    "author": "Oscar Bartle",
    "version": (0,2,1),     
    "blender": (4,2,5),
    "location": "3D Viewport > Sidebar > Woody",
    "description": "A pipeline tool",
    "category": "Development",
}

import os
import re
import uuid
import shutil
import subprocess
import bpy
import json
from pathlib import Path

#===============
# Global Variables
#===============

_json_cache = None  # Global cache

#===============
# Functions
#===============

# Create folders

def create_folders_subfolders(folders, base_path):
    for main_folder, subfolders in folders.items():
        main_path = base_path / main_folder
        main_path.mkdir(parents=True, exist_ok=True)

        if isinstance(subfolders, dict):
            create_folders_subfolders(subfolders, main_path)
        elif isinstance(subfolders, list): 
            for subfolder in subfolders:
                (main_path / subfolder).mkdir(parents=True, exist_ok=True)

# Create enums based on json

def load_json_data(context):
    global _json_cache
    if _json_cache is None:
        print("================= Loading new JSON data... =================")
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        base_path = Path(bpy.path.abspath(directory))
        json_file = base_path / "projStruc.json"

        if not json_file.exists():
            print("ERROR: JSON file not exist.")
            return {}

        with open(json_file, "r", encoding="utf-8") as file:
            _json_cache = json.load(file)
        print("================= CACHE LOADED =================")
        return _json_cache
    print("Using cached JSON.")
    return _json_cache

def get_root_folders(self, context):
    data = load_json_data(context)
    return [(key, key, f"Root folder: {key}") for key, value in data.items() if value.get("type") == "root"] or [("NONE", "None", "No root folders found")]

def get_group_folders(self, context):
    data = load_json_data(context)
    selected_root = context.scene.woody.root_folder

    if selected_root not in data:
        return [("NONE", "None", "No groups found")]

    root_contents = data[selected_root]["contents"]
    return [(key, key, f"Group: {key}") for key, value in root_contents.items() if value.get("type") == "group"] or [("NONE", "None", "No groups found")]

def get_asset_folders(self, context):
    data = load_json_data(context)
    selected_root = context.scene.woody.root_folder
    selected_group = context.scene.woody.group_folder

    if selected_root not in data:
        return [("NONE", "None", "No assets found")]

    group_contents = data[selected_root]["contents"].get(selected_group, {}).get("contents", {})
    return [(key, key, f"Asset: {key}") for key, value in group_contents.items() if value.get("type") == "asset"] or [("NONE", "None", "No assets found")]

def get_type_folders(self, context):
    data = load_json_data(context)
    selected_root = context.scene.woody.root_folder
    selected_group = context.scene.woody.group_folder
    selected_asset = context.scene.woody.asset_folder

    if selected_root not in data:
        return [("NONE", "None", "No types found")]

    asset_contents = data[selected_root]["contents"].get(selected_group, {}).get("contents", {}).get(selected_asset, {}).get("contents", {})
    return [(key, key, f"Type: {key}") for key, value in asset_contents.items() if value.get("type") == "type"] or [("NONE", "None", "No types found")]

# Generate and save json folder structure

def get_folder_structure(base_path, depth=0, exclude_names=("_publish",)):
    folder_dict = {}

    for item in os.listdir(base_path):
        if item in exclude_names:
            continue

        item_path = os.path.join(base_path, item)

        if os.path.isdir(item_path):
            folder_dict[item] = {
                "type": get_folder_type(depth),
                "contents": get_folder_structure(item_path, depth + 1, exclude_names)
            }

    return folder_dict

def get_folder_type(depth):
    if depth == 0:
        return "root"
    elif depth == 1:
        return "group"
    elif depth == 2:
        return "asset"
    else:
        return "type"

def save_structure_to_json(base_path):

    folder_structure = get_folder_structure(base_path)


    output_file = os.path.join(base_path, "projStruc.json")

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(folder_structure, json_file, indent=4)

    print(f"Folder structure saved to: {output_file}")

    global _json_cache
    _json_cache = None

# .blend functions

def new_blend(blender_exe, new_file_name):

    blender_exe_path = Path(blender_exe)
    if not blender_exe_path.exists():
        print(f"❌ Error: Blender executable not found at {blender_exe}")
        return

    if bpy.data.filepath:
        current_directory = Path(bpy.path.abspath("//"))
    else:
        current_directory = Path(os.path.expanduser("~")) / "Blender_New_Files"
        current_directory.mkdir(parents=True, exist_ok=True)

    new_file_path = current_directory / new_file_name

    command = [
        str(blender_exe_path),
        "--background",
        "--python-expr",
        f"import bpy; bpy.ops.wm.save_mainfile(filepath=r'{new_file_path}')"
    ]

    subprocess.Popen(command)

    open_command = [
        str(blender_exe_path),
        str(new_file_path)
    ]

    subprocess.Popen(open_command)

    print(f"Opening new Blender instance with file: {new_file_path}")

def open_blend(blender_exe, blend_file_path):
    blender_exe_path = Path(blender_exe)
    blend_file = Path(blend_file_path)

    if not blender_exe_path.exists():
        print(f"❌ Error: Blender executable not found at {blender_exe}")
        return

    if not blend_file.exists():
        print(f"❌ Error: .blend file not found at {blend_file_path}")
        return

    subprocess.Popen([str(blender_exe_path), str(blend_file)])

    print(f"Opening new Blender instance with file: {blend_file_path}")

def save_current_scene():

    if bpy.data.filepath:
        bpy.ops.wm.save_mainfile()
        print(f"Scene saved: {bpy.data.filepath}")
    else:
        print("Scene has not been saved before. Skipping save.")

def incremental_save(new_name):
    
    if not bpy.data.filepath:
        print("❌ Error: Scene has not been saved before. Save it first.")
        return
    
    current_path = Path(bpy.data.filepath)
    directory = current_path.parent
    extension = current_path.suffix

    print("Checking files in directory:", directory)

    version_pattern = re.compile(rf"{re.escape(new_name)}_v(\d+){re.escape(extension)}$")

    existing_versions = []
    for file in directory.iterdir():
        match = version_pattern.match(file.name)
        if match:
            existing_versions.append(int(match.group(1)))

    print("Existing versions found:", existing_versions)

    next_version = max(existing_versions, default=0) + 1

    new_filename = f"{new_name}_v{next_version}{extension}"
    new_file_path = directory / new_filename

    shutil.copy2(current_path, new_file_path)

    print(f"Duplicated and renamed scene as: {new_file_path}")

def restart_blend_file():

    current_file = bpy.data.filepath

    if not current_file:
        print("No file is currently open.")
        return
    
    bpy.ops.wm.open_mainfile(filepath=current_file)

# context

def context_names():
    if not bpy.data.filepath:
        print("[context_names] 🚨 No filepath set — save your .blend file first.")
        return "ROOT", "GROUP", "ASSET", "TYPE"
     
    current_path = Path(bpy.data.filepath)
    directory = current_path.parent
   

    directory = str(directory)
    directory = directory.split("\\")

    if len(directory) < 4:
       print(f"[context_names] 🚨 Not enough directories in path: {directory}")
       return "ROOT", "GROUP", "ASSET", "TYPE"

    root = directory[-4]
    group = directory[-3]
    asset = directory[-2]
    type_ = directory[-1]

    return root, group, asset, type_

# catalogs

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

#===============
# Properties & Preferences
#===============

class Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    directory: bpy.props.StringProperty(name= "Directory", subtype='FILE_PATH', description="The directory of your project") # type: ignore
    blenderVersion: bpy.props.StringProperty(name= "EXE Path", subtype='FILE_PATH', description="Path to your blender.exe") # type: ignore

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_props = scene.woody
        
        pathsBox = layout.box()
        pathsBox.label(text="Paths")
        pathsBox.scale_y = 0.65

        layout.prop(self, "directory")
        layout.prop(self, "blenderVersion")

        projectBox = layout.box()
        projectBox.label(text="Project")
        projectBox.scale_y = 0.65

        row1 = self.layout.row()
        row1.operator("pipe.create_project", text="Create Project", icon="WORLD")
        row1.operator("wm.save_userpref", text="Save Project", icon="DOCUMENTS")

def get_preferences():
    preferences = bpy.context.preferences.addons[__name__].preferences
    return preferences

def get_directory():
    preferences = get_preferences()
    return preferences.directory

def get_blender_version():
    preferences = get_preferences()
    return preferences.blenderVersion

class MyProperties(bpy.types.PropertyGroup):
    
    root_folder: bpy.props.EnumProperty(name="Root", description="Select a root", items=get_root_folders,) # type: ignore
    group_folder: bpy.props.EnumProperty(name="Group", description="Select a group", items=get_group_folders,) # type: ignore
    asset_folder: bpy.props.EnumProperty(name="Asset", description="Select an asset", items=get_asset_folders,) # type: ignore
    type_folder: bpy.props.EnumProperty(name="Type", description="Select a type", items=get_type_folders,) # type: ignore

    group: bpy.props.StringProperty(name="Group", description="Name of new group") # type: ignore
    asset: bpy.props.StringProperty(name="Asset", description="Name of new asset") # type: ignore
    shot: bpy.props.StringProperty(name="Shot", description="Name of new shot") # type: ignore
    
    typeAsset: bpy.props.EnumProperty(
        name="Type",
        description="Choose an asset type",
        items=[
            ("ref", "ref", "ref"),
            ("model", "model", "model"),
            ("lookdev", "lookdev", "lookdev")
        ],
        default="model"  # Default value
    ) # type: ignore
    typeShot: bpy.props.EnumProperty(
        name="Shot",
        description="Choose an shot type",
        items=[
            ("layout", "layout", "layout"),
            ("animation", "animation", "animation"),
            ("FX", "FX", "FX"),
            ("lighting", "lighting", "lighting")
        ],
        default="layout"  # Default value
    ) # type: ignore

#===============
# Functions With Properties
#===============

def publish(collection_name, tags):
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

def create_blend_with_collection(file_name, collection_name, target_directory):

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

def open_publish_blend_file(file_path):

    blender_exe = get_blender_version()

    if not os.path.exists(file_path):
        print(f"❌ Error: File does not exist - {file_path}")
        return

    subprocess.Popen([blender_exe, file_path], close_fds=True, start_new_session=True)

    print(f"✅ Opened Blender in a separate instance with file: {file_path}")

def select_objects_in_selected_collection(collection_name):

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

def export_selection_to_usd(export_path, export_format='USD'):

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

def create_publish_workspace(workspace_name="My Custom Workspace"):

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

def rename_workspace(old_name, new_name):

    if old_name in bpy.data.workspaces:
        bpy.data.workspaces[old_name].name = new_name
        print(f"✅ Workspace renamed from '{old_name}' to '{new_name}'")
    else:
        print(f"✅ Workspace '{old_name}' not found!")

def delete_collection_contents(collection_name):

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

def import_usdc_to_collection(file_path, collection_name):

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

#===============
# Operators
#===============

class PIPE_OT_create_project(bpy.types.Operator):
    # Creates a new project with the correct folder structure in the base project directory

    bl_idname = "pipe.create_project"
    bl_label = "Create a new project"

    def execute(self, context):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        base_path = Path(bpy.path.abspath(directory))

        # Dictionary of folders and subfolders
        folders = {
                "assets": [],
                "shots": [],
                "_publish": [],
        }

        create_folders_subfolders(folders, base_path)

        return {"FINISHED"}
    
class PIPE_OT_create_group(bpy.types.Operator):
    bl_idname = "pipe.create_group"
    bl_label = "Create Group"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        base_path = Path(bpy.path.abspath(directory)) 
        save_structure_to_json(base_path)

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        base_path = Path(bpy.path.abspath(directory))
        base_path = Path(base_path) / my_props.root_folder

        # Dictionary of folders and subfolders
        if my_props.root_folder == "assets":
            folders = {
                my_props.group:{
                    "base": ["ref", "model", "lookdev", "rigging"]
                }

            }
        else:
            folders = {
                my_props.group:{
                    "base": ["ref", "layout", "FX", "lighting", "animation"]
                }

            }

        create_folders_subfolders(folders, base_path)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        my_props = context.scene.woody

        layout.prop(my_props, "root_folder")
        layout.prop(my_props, "group")

class PIPE_OT_create_asset(bpy.types.Operator):
    bl_idname = "pipe.create_asset"
    bl_label = "Create Asset"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        save_current_scene()

        base_path = Path(bpy.path.abspath(directory)) 
        save_structure_to_json(base_path) 

        data = load_json_data(context)
        if "assets" in data:
            scene.woody.root_folder = "assets" 
            groups = get_group_folders(self, context)
            if groups and groups[0][0] != "NONE":
                scene.woody.group_folder = groups[0][0] 

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()
        blenderVersion = get_blender_version()

        base_path = Path(bpy.path.abspath(directory))
        base_path = Path(base_path) / "assets" / my_props.group_folder

        folders = {
                my_props.asset: ["ref", "model", "lookdev", "rigging"],
        }

        create_folders_subfolders(folders, base_path)

        base_path = Path(base_path) / my_props.asset / my_props.typeAsset
        file_name = f"{my_props.asset}_{my_props.typeAsset}_latest.blend"
        full_path = base_path / file_name
        new_blend(blender_exe=blenderVersion, new_file_name=full_path)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        my_props = context.scene.woody

        layout.prop(my_props, "group_folder")
        layout.prop(my_props, "asset")
        layout.prop(my_props, "typeAsset")

class PIPE_OT_create_shot(bpy.types.Operator):
    bl_idname = "pipe.create_shot"
    bl_label = "Create Shot"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        save_current_scene()

        base_path = Path(bpy.path.abspath(directory)) 
        save_structure_to_json(base_path)  

        data = load_json_data(context)
        if "shots" in data:
            scene.woody.root_folder = "shots" 
            groups = get_group_folders(self, context)
            if groups and groups[0][0] != "NONE":
                scene.woody.group_folder = groups[0][0] 

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()
        blenderVersion = get_blender_version()

        base_path = Path(bpy.path.abspath(directory))
        base_path = Path(base_path) / "shots" / my_props.group_folder

        # Dictionary of folders and subfolders
        folders = {
                my_props.shot: ["ref", "layout", "FX", "lighting", "animation"],
        }

        create_folders_subfolders(folders, base_path)

        base_path = Path(base_path) / my_props.shot / my_props.typeShot
        file_name = f"{my_props.shot}_{my_props.typeShot}_latest.blend"
        full_path = base_path / file_name
        new_blend(blender_exe=blenderVersion, new_file_name=full_path)

        return {"FINISHED"}


    def draw(self, context):
        layout = self.layout
        my_props = context.scene.woody

        layout.prop(my_props, "group_folder")
        layout.prop(my_props, "shot")
        layout.prop(my_props, "typeShot")

class PIPE_OT_open_asset(bpy.types.Operator):

    bl_idname = "pipe.open_asset"
    bl_label = "Open Asset"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()

        save_current_scene()

        base_path = Path(bpy.path.abspath(directory))
        save_structure_to_json(base_path)  # Save the JSON before showing the popup

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        scene = context.scene
        my_props = scene.woody

        directory = get_directory()
        blenderVersion = get_blender_version()

        base_path = Path(bpy.path.abspath(directory)) / my_props.root_folder / my_props.group_folder / my_props.asset_folder / my_props.type_folder
        file_name = f"{my_props.asset_folder}_{my_props.type_folder}_latest.blend"
        full_path = base_path / file_name
        open_blend(blender_exe=blenderVersion, blend_file_path=full_path)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        my_props = context.scene.woody

        layout.prop(my_props, "root_folder")
        layout.prop(my_props, "group_folder")
        layout.prop(my_props, "asset_folder")
        layout.prop(my_props, "type_folder")

class PIPE_OT_version_up(bpy.types.Operator):

    bl_idname = "pipe.save_asset"
    bl_label = "Save Asset"

    def execute(self, context):

        save_current_scene()

        current_path = Path(bpy.data.filepath)
        filename = current_path.stem
        print(filename)
        filename = filename.replace("_latest" , "")

        incremental_save(new_name=filename)

        return {"FINISHED"}

class PIPE_OT_publish_prep(bpy.types.Operator):
    bl_idname = "pipe.publish_prep"
    bl_label = "Publish Asset"

    def execute(self, context):
        
        directory = get_directory()
        directory = Path(directory)

        root, group, asset, type_ = context_names()
        collection_name = root + "_" + group + "_" + asset + "_" + type_
        tags = [root, group, asset, type_]

        file_path = Path(directory) / "_publish" / "blender_assets.cats.txt"
        add_to_catalog_file(collection_name, file_path)

        publish(collection_name, tags)

        export_dir = directory / "_publish" / "blends"
        export_filename = collection_name + ".blend"
        export_path = export_dir / export_filename

        create_blend_with_collection(export_filename, collection_name, export_dir)
        
        open_publish_blend_file(export_path)

        select_objects_in_selected_collection(collection_name)

        export_geo_dir = directory / "_publish" / "geo" / collection_name
        export_file = collection_name + ".usdc"
        export_geo_path = export_geo_dir / export_file

        export_selection_to_usd(str(export_geo_path), export_format="USDC")

        save_current_scene()

        restart_blend_file()

        return {"FINISHED"}

class PIPE_OT_create_publish_workspace(bpy.types.Operator):
    bl_idname = "pipe.create_publish_workspace"
    bl_label = "Publish Asset"

    def execute(self, context):

        create_publish_workspace("Layout")
        rename_workspace("Layout", "Publish")

        return {"FINISHED"}

class PIPE_OT_publish(bpy.types.Operator):

    bl_idname = "pipe.publish_asset"
    bl_label = "Publish Asset"

    def execute(self, context):

        directory = get_directory()
        directory = Path(directory)

        file_path = bpy.data.filepath
        file_name = os.path.basename(file_path)
        file_name = file_name.replace(".blend", "")

        collection_name = file_name
        
        import_geo_dir = directory / "_publish" / "geo" / collection_name
        import_file = collection_name + ".usdc"
        import_geo_path = os.path.join(import_geo_dir, import_file)

        delete_collection_contents(collection_name)
        import_usdc_to_collection(import_geo_path, collection_name)

        return {"FINISHED"}

class PIPE_FVpublish(bpy.types.Operator):
    bl_idname = "pipe.fv_publish"
    bl_label = "FV Publish"
    def execute(self, context):
        return {"FINISHED"}

#===============
# Panels
#===============

# Context

class VIEW3D_PT_context(bpy.types.Panel):
     
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Context"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout

        root, group, asset, type_ = context_names()
         
        rootBox = layout.box()
        rootBox.label(text=f"root - {root}", icon="OUTLINER")
        rootBox.scale_y = 0.75

        groupBox = layout.box()
        groupBox.label(text=f"group - {group}", icon="GROUP_VERTEX")
        groupBox.scale_y = 0.75

        assetBox = layout.box()
        assetBox.label(text=f"asset - {asset}", icon="MESH_CUBE")
        assetBox.scale_y = 0.75

        typeBox = layout.box()
        typeBox.label(text=f"type - {type_}", icon="OUTLINER_DATA_POINTCLOUD")
        typeBox.scale_y = 0.75

# Asset

class VIEW3D_PT_assets_shots(bpy.types.Panel):
     
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Assets/Shots"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout

        newAssetBox = layout.box()
        newAssetBox.label(text="New")
        newAssetBox.scale_y = 0.65

        layout.operator("pipe.create_group", text="New Group", icon="GROUP_VERTEX")

        row1 = self.layout.row()
        row1.operator("pipe.create_asset", text="New Asset", icon="OUTLINER_OB_META")
        row1.operator("pipe.create_shot", text="New Shot", icon="VIEW_CAMERA")

        fileBox = layout.box()
        fileBox.label(text="File")
        fileBox.scale_y = 0.65

        row2 = self.layout.row()
        row2.operator("pipe.open_asset", text="Open", icon="COPY_ID")
        row2.operator("pipe.save_asset", text="Save", icon="NODE_COMPOSITING")
        
        publishBox = layout.box()
        publishBox.label(text="Publish")
        publishBox.scale_y = 0.65

        row1 = layout.row()
        row1.operator("pipe.publish_prep", text="Publish Prep", icon="SURFACE_NSPHERE")
        row1.operator("pipe.create_publish_workspace", text="Workspace", icon="WINDOW")

        layout.operator("pipe.publish_asset", text="Publish", icon="DISK_DRIVE")

        row2 = layout.row()
        row2.operator("pipe.fv_publish", text="FV_Publish2", icon="DISK_DRIVE")
        
#===============              
# Registration
#===============              
        
classes = [
    MyProperties,
    PIPE_OT_create_project,
    PIPE_OT_create_group,
    PIPE_OT_create_asset,
    PIPE_OT_create_shot,
    PIPE_OT_open_asset,
    PIPE_OT_version_up,
    PIPE_OT_publish,
    PIPE_OT_publish_prep,
    PIPE_OT_create_publish_workspace,
    PIPE_FVpublish,
    Preferences,
    VIEW3D_PT_context,
    VIEW3D_PT_assets_shots
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        bpy.types.Scene.woody = bpy.props.PointerProperty(type= MyProperties)

def unregister():
    for cls in reversed(classes):  # reversed is safer for dependencies
        bpy.utils.unregister_class(cls)
    
    if hasattr(bpy.types.Scene, "woody"):
        del bpy.types.Scene.woody

if __name__ == "__main__":
    register()
