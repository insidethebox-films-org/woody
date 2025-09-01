from ...utils import *

import subprocess
from pathlib import Path

def open_blend(blender_exe, blend_file_path, config_path):
    blender_exe_path = Path(blender_exe)
    blend_file = Path(blend_file_path)

    if not blender_exe_path.exists():
        print(f"❌ Error: Blender executable not found at {blender_exe}")
        return

    if not blend_file.exists():
        print(f"❌ Error: .blend file not found at {blend_file_path}")
        return

    if config_path:
        config_script = generate_config_script(config_path)
        subprocess.Popen([str(blender_exe_path), str(blend_file), '--python', str(config_script)])
    else:
        subprocess.Popen([str(blender_exe_path), str(blend_file)])

    print(f"Opening new Blender instance with file: {blend_file_path}")