"""
Scene properties for the Woody Blender addon.
Defines all custom properties attached to scenes for publish functionality.
"""

import bpy


def register_properties():
    """Register all scene properties for the addon."""
    bpy.types.Scene.woody_publish_id = bpy.props.StringProperty(
        name="Publish ID",
        description="Paste publish ID in format: id#ver:version",
        default=""
    )
    
    bpy.types.Scene.woody_loaded_publishes_count = bpy.props.IntProperty(
        name="Loaded Publishes Count",
        description="Number of loaded published assets in scene",
        default=0
    )
    
    bpy.types.Scene.woody_loaded_publishes_display = bpy.props.StringProperty(
        name="Loaded Publishes Display",
        description="Formatted display of loaded published assets",
        default="No published assets loaded"
    )
    
    bpy.types.Scene.woody_loaded_publishes_data = bpy.props.StringProperty(
        name="Loaded Publishes Data",
        description="JSON data of loaded publishes for UI buttons",
        default="[]"
    )


def unregister_properties():
    """Unregister all scene properties for the addon."""
    del bpy.types.Scene.woody_publish_id
    del bpy.types.Scene.woody_loaded_publishes_count
    del bpy.types.Scene.woody_loaded_publishes_display
    del bpy.types.Scene.woody_loaded_publishes_data