import re
import shutil
import bpy
from pathlib import Path

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