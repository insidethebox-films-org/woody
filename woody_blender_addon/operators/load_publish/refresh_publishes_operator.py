"""
Refresh Loaded Publishes Operator for the Woody Blender addon.
Handles refreshing the display of loaded published assets in the scene.
"""

import bpy
from ...utils.publish_utils import refresh_loaded_publishes_data


class WOODY_OT_refresh_loaded_publishes(bpy.types.Operator):
    bl_idname = "woody.refresh_loaded_publishes"
    bl_label = "Refresh Loaded Publishes"
    bl_description = "Refresh the list of loaded published assets"

    def execute(self, context):
        # Use the shared utility function to refresh the data
        refresh_loaded_publishes_data(context)
        
        loaded_count = getattr(context.scene, 'woody_loaded_publishes_count', 0)
        if loaded_count > 0:
            self.report({'INFO'}, f"Refreshed: Found {loaded_count} loaded publishes")
        else:
            self.report({'INFO'}, "No linked publishes found in scene")
        
        return {'FINISHED'}