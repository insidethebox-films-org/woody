from ..utils import *

import os
import bpy

class PIPE_OT_apply_render_config(bpy.types.Operator):
    bl_idname = "pipe.apply_render_config"
    bl_label = "Apply Render Config"
    bl_description = "Apply settings from projConfig.json"

    def execute(self, context):
        blend_path = bpy.data.filepath
        if not blend_path:
            self.report({'WARNING'}, "⚠️ Could not set path — are you in a valid asset/shot file?")
            return {'CANCELLED'}
        
        project_root = get_directory()

        if not project_root:
            self.report({'WARNING'}, "⚠️ Could not find project root")
            return {'CANCELLED'}

        config_path = os.path.join(project_root, "projConfig.json")
        if not os.path.isfile(config_path):
            self.report({'WARNING'}, f"⚠️ No projConfig.json found at: {config_path}")
            return {'CANCELLED'}

        apply_render_config(config_path)
        self.report({'INFO'}, f"✅ Render config applied from {config_path}")
        return {'FINISHED'}
    