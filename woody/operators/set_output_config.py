from ..lib.blender.get_preferences import get_directory
from ..lib.blender.set_render_output_to_cg import set_render_output_to_cg

import bpy

class PIPE_OT_set_output_cg(bpy.types.Operator):
    bl_idname = "pipe.set_output_cg"
    bl_label = "Set Output to CG Folder"
    bl_description = "Set render output path to the cg folder"

    def execute(self, context):
        print("GET DIR: ",get_directory())
        success = set_render_output_to_cg()
        if success:
            self.report({'INFO'}, "✅ Render output path set to CG folder")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "⚠️ Could not set path — are you in a valid asset/shot file?")
            return {'CANCELLED'}
