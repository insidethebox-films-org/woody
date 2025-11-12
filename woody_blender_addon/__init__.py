bl_info = {
    "name": "Woody",
    "author": "Oscar Bartle",
    "version": (0, 0, 1),
    "blender": (4, 2, 5),
    "location": "3D Viewport > Sidebar > Woody",
    "description": "A pipeline tool",
    "category": "Development",
}

import bpy 
from .panel import VIEW3D_PT_context
from .preferences import WoodyAddonPreferences
from .operators.version_up import WOODY_OT_version_up
from .operators.publish.publish_operator import WOODY_OT_publish
from .operators.load_publish import WOODY_OT_load_publish, WOODY_OT_override_publish, WOODY_OT_refresh_loaded_publishes, WOODY_OT_delete_publish
from .properties import register_properties, unregister_properties


# =============== Registration ===============

classes = [
    VIEW3D_PT_context,
    WOODY_OT_version_up,
    WoodyAddonPreferences,
    WOODY_OT_publish,
    WOODY_OT_load_publish,
    WOODY_OT_refresh_loaded_publishes,
    WOODY_OT_override_publish,
    WOODY_OT_delete_publish
]


def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            print(f"Failed to register {cls.__name__}: {str(e)}")
    
    # Register scene properties
    register_properties()

def unregister():
    # Unregister scene properties
    unregister_properties()
    
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            print(f"Failed to unregister {cls.__name__}: {str(e)}")

if __name__ == "__main__":
    register()
