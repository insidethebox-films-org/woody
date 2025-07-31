import os
import zipfile
from pathlib import Path
import subprocess
import time
import psutil

#Update all paths to the ones you work with. 
#Each line will have a comment "UPDATE".

# Paths
repo_path = r"C:\Users\Oscar\Documents\github\woody"  #UPDATE path to the location of your cloned repo
zip_name = "woody.zip"
zip_path = os.path.join(repo_path, zip_name)
int_file = os.path.join(repo_path, "__int__.py")
blender_exe = r"D:\_software\blender-4.2.5-windows-x64\blender.exe" #UPDATE path to the location of your blender.exe

addon_module_name = "woody"  # Name used to register the addon
addon_zip_path = zip_path.replace("\\", "/")  # Use forward slashes for Blender compatibility

def close_blender():
    """Find and kill any Blender processes."""
    for proc in psutil.process_iter(['pid', 'name']):
        if 'blender.exe' in proc.info['name'].lower():
            print(f"Closing Blender (PID {proc.pid})...")
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except psutil.TimeoutExpired:
                proc.kill()

def delete_zip():
    """Delete the existing woody.zip if it exists."""
    if os.path.exists(zip_path):
        print("Deleting existing zip file...")
        os.remove(zip_path)

def create_zip():
    """Create woody.zip from __init__.py."""
    print("Creating new zip file...")
    addon_folder = Path(repo_path) / "woody"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for file in addon_folder.rglob("*"):
            z.write(file, file.relative_to(addon_folder.parent))

    print("Zip file created.")

def install_addon():
    """Run Blender in background to uninstall, reinstall, and configure the addon."""
    print("Installing addon in Blender...")

    blender_python = f"""
import bpy
import addon_utils

addon_name = "{addon_module_name}"

# Disable if already enabled
if addon_name in bpy.context.preferences.addons:
    print(f"Disabling addon '{{addon_name}}'...")
    addon_utils.disable(addon_name)

# Remove if already installed
for mod in list(bpy.context.preferences.addons.keys()):
    if mod == addon_name:
        print(f"Removing addon '{{addon_name}}'...")
        bpy.ops.preferences.addon_remove(module=addon_name)

# Install
print("Installing addon from zip...")
bpy.ops.preferences.addon_install(filepath="{addon_zip_path}", overwrite=True)

# Enable
print("Enabling addon...")
bpy.ops.preferences.addon_enable(module=addon_name)

# Set preferences
prefs = bpy.context.preferences.addons[addon_name].preferences
prefs.directory  = r"\\\\100.113.50.90\projects\PUD\dev\oscarProject" #UPDATE to location of project you are working on.
prefs.blenderVersion  = r"D:\_software\blender-4.2.5-windows-x64\blender.exe" #UPDATE path to the location of your blender.exe

# Save preferences
bpy.ops.wm.save_userpref()
print("Addon installed and configured.")
"""
    subprocess.run([blender_exe, "--background", "--factory-startup", "--python-expr", blender_python])

def launch_blender():
    """Launch Blender."""
    print("Launching Blender...")
    subprocess.Popen([blender_exe])

if __name__ == "__main__":
    close_blender()
    time.sleep(2)  # Wait for Blender to fully shut down
    delete_zip()
    create_zip()
    install_addon()
    launch_blender()
