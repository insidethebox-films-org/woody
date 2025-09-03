from ..utils.context import context_names

import bpy
import json
from pathlib import Path

class PIPE_OT_set_frame_range(bpy.types.Operator):
    bl_idname = "pipe.set_frame_range"
    bl_label = "Set Frame Range"
    bl_description = "Update scene frame range and shot config file"

    frame_start: bpy.props.IntProperty(name="Start Frame")# type:ignore
    frame_end: bpy.props.IntProperty(name="End Frame")# type:ignore

    def execute(self, context):
        scene = context.scene
        root, group, asset, type_ = context_names()

        if root=="shots":
            config_path = Path(bpy.path.abspath("//")).parent / "shot_config.json"

            data = {}
            if config_path.exists():
                with open(config_path, "r") as f:
                    data = json.load(f)

            # Update with UI values
            data["frame_start"] = scene.shot_frame_start
            data["frame_end"] = scene.shot_frame_end

            with open(config_path, "w") as f:
                json.dump(data, f, indent=4)

        # Apply to scene
        scene.frame_start = scene.shot_frame_start
        scene.frame_end = scene.shot_frame_end

        self.report({'INFO'}, "Frame range updated")
        return {'FINISHED'}