import os
import zipfile
from pathlib import Path

def update_zip_dev(addon_zip: str) -> bool:
    """Updates the addon zip file for development"""
    
    addon_dir = Path(__file__).resolve().parents[4] / "woody_blender_addon"
    
    print(f"Current file: {__file__}")
    print(f"Addon exists: {addon_dir.exists()}")
    
    if not addon_dir.exists():
        print(f"ERROR: Addon directory not found!")
        return False
    
    try:
        if os.path.exists(addon_zip):
            os.remove(addon_zip)
            print(f"\nRemoved old zip: {addon_zip}")
        
        os.makedirs(os.path.dirname(addon_zip), exist_ok=True)

        file_count = 0
        
        with zipfile.ZipFile(addon_zip, 'w', zipfile.ZIP_DEFLATED) as z:
            for file in sorted(addon_dir.rglob('*')):
                
                # Only files
                if file.is_file():
                    relative_path = file.relative_to(addon_dir.parent)
                    
                    with open(file, 'rb') as f:
                        file_data = f.read()
                    
                    zip_path = str(relative_path).replace('\\', '/')
                    z.writestr(zip_path, file_data)
                    file_count += 1
        
        print(f"Zip created!")
        print(f"Files: {file_count}")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False