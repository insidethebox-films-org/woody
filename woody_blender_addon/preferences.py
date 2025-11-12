from bpy.props import StringProperty #type: ignore
from bpy.types import AddonPreferences #type: ignore

class WoodyAddonPreferences(AddonPreferences):
    bl_idname = __name__.split('.')[0]  # This gets the addon name (woody_blender_addon)
    
    mongodb_address: StringProperty(
        name="MongoDB Address",
        description="MongoDB connection string (e.g., mongodb://100.113.50.90:2222)",
        default=""
    )#type: ignore
    
    project_name: StringProperty(
        name="Project Name", 
        description="Name of the current project database",
        default=""
    )#type: ignore
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "mongodb_address")
        layout.prop(self, "project_name")