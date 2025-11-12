import os
import subprocess

def create_blend_file(executable: str, blend_path: str) -> bool:
    """Creates a new blend file
    
    Args:
        executable (str): Path to Blender executable
        blend_path (str): Path to the blend file to create
    
    Returns:
        bool: True if blend file was created successfully
    """
    
    try:
        cmd = (
            f'"{executable}" --background '
            f'--python-expr "import bpy; bpy.ops.wm.save_as_mainfile(filepath=r\'{blend_path}\')"'
        )
        subprocess.run(cmd, shell=True, check=True)

        if os.path.exists(blend_path):
            print(f"Successfully created blend file at: {blend_path}")
            return True
        print(f"File creation reported success but file not found at: {blend_path}")
        return False

    except subprocess.CalledProcessError as e:
        print(f"Blender process error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error creating blend file: {str(e)}")
        return False

