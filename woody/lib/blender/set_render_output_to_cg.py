from ...preferences import *
from ...context import *
from ..folders import get_next_version_folder

import bpy

from pathlib import Path


def set_render_output_to_cg():
    if not bpy.data.filepath:
        print("[set_render_output_to_cg] 🚨 File not saved yet.")
        return False

    root, group, asset, type_ = context_names()

    # Validate structure
    if root not in {"assets", "shots"} or group == "GROUP" or asset == "ASSET":
        print(f"[set_render_output_to_cg] 🚨 Unexpected path: {root}/{group}/{asset}")
        return False

    current_path = Path(bpy.data.filepath)

    # Fix: Avoid duplicating the root folder in path
    cg_folder = current_path.parents[3] / group / asset / "cg"

    # Create folder if needed
    cg_folder.mkdir(parents=True, exist_ok=True)

    # 🆕 Get next version folder inside cg/
    version_folder = get_next_version_folder(cg_folder)
    version_folder.mkdir(parents=True, exist_ok=True)

    # Set output path
    bpy.context.scene.render.filepath = str(version_folder) + "/"
    print(f"[set_render_output_to_cg] ✅ Output path set to {bpy.context.scene.render.filepath}")
    return True