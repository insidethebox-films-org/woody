import subprocess
import os
import ctypes
import argparse
import shutil
from pathlib import Path

# --- CONFIGURATION ---
BLENDER_ROOT = Path(r"D:\_software\blender-5.0.1-windows-x64_Copy")
BLENDER_EXE = BLENDER_ROOT / "blender.exe"

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def sync():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Force update dependencies")
    args = parser.parse_args()

    if not is_admin():
        print("!!! ERROR: Please run this terminal as ADMINISTRATOR.")
        return

    # --- PATH CALCULATIONS ---
    # Current file: C:\...\woody\woody\dcc\blender\sync_blender.py
    # Project root: C:\...\woody\ (contains pyproject.toml)
    # Source folder: C:\...\woody\woody\ (contains __init__.py)
    
    script_path = Path(__file__).resolve()
    # Go up 4 levels to get from blender/dcc/woody/woody to the ROOT woody
    project_root = script_path.parents[3] 
    source_folder = project_root / "woody"

    if not (project_root / "pyproject.toml").exists():
        print(f"!!! ERROR: Could not find pyproject.toml at {project_root}")
        return

    # 1. Find Blender's Python
    python_exe = next(BLENDER_ROOT.rglob("python.exe"), None)
    if not python_exe:
        print(f"Could not find python.exe in {BLENDER_ROOT}")
        return

    # 2. Get Blender's Modules Path
    print("Querying Blender for local scripts path...")
    query = "import bpy; print('PATH_START' + bpy.utils.user_resource('SCRIPTS', path='modules', create=True) + 'PATH_END')"
    process = subprocess.run([str(BLENDER_EXE), "-b", "--factory-startup", "--python-expr", query], 
                            capture_output=True, text=True)
    modules_path = Path(process.stdout.split("PATH_START")[1].split("PATH_END")[0].strip())

    # 3. Update Pip and Dependencies
    print(f"--- Syncing Dependencies to Blender ---")
    
    # Optional: Upgrade pip inside Blender first
    subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"], check=False)

    # Install the root project (this pulls in pymongo, customtkinter, etc.)
    pip_cmd = [str(python_exe), "-m", "pip", "install", str(project_root)]
    if args.update:
        pip_cmd.append("--upgrade")
    
    print(f"Running: {' '.join(pip_cmd)}")
    subprocess.run(pip_cmd, check=True)

    # 4. Link 'woody' code via Junction
    # This link goes into the portable/scripts/modules folder
    target_link = modules_path / "woody"
    
    if target_link.exists() or target_link.is_symlink():
        print(f"Removing existing link at: {target_link}")
        # 'rmdir' is the safest way to remove a Junction link on Windows
        subprocess.run(['cmd', '/c', 'rmdir', '/s', '/q', str(target_link)], shell=True)

    print(f"--- Creating Live Link: {target_link} <==> {source_folder} ---")
    subprocess.run(['cmd', '/c', 'mklink', '/J', str(target_link), str(source_folder)], check=True)

    print("\n✅ Sync Complete! Restart Blender and test 'import woody'.")

if __name__ == "__main__":
    sync()