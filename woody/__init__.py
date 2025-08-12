bl_info = {
    "name": "Woody",
    "author": "Oscar Bartle",
    "version": (0, 2, 3),
    "blender": (4, 2, 5),
    "location": "3D Viewport > Sidebar > Woody",
    "description": "A pipeline tool",
    "category": "Development",
}

import bpy
from .properties import MyProperties
from .preferences import Preferences_Properties
from .utils import *
from .operators import (
    PIPE_OT_create_project, PIPE_OT_create_group, PIPE_OT_create_asset,
    PIPE_OT_create_shot, PIPE_OT_open_asset, PIPE_OT_version_up,
    PIPE_OT_publish, PIPE_OT_set_output_cg, PIPE_OT_apply_render_config,
    PIPE_OT_render_with_prompt, PIPE_OT_set_frame_range, PIPE_OT_open_publish, PIPE_OT_clear_enum,
    PIPE_OT_override_collection
)
from .panels import (
    VIEW3D_PT_context, VIEW3D_PT_assets_shots, VIEW3D_PT_settings, VIEW3D_PT_publish_browser
)
class preferences_panel(Preferences_Properties, bpy.types.AddonPreferences):
    bl_idname = __package__ 

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_props = scene.woody

        pathsBox = layout.box()
        pathsBox.label(text="Paths")
        pathsBox.scale_y = 0.65
        layout.prop(self, "directory")
        layout.prop(self, "blenderVersion")

        projectBox = layout.box()
        projectBox.label(text="Project")
        projectBox.scale_y = 0.65

        row1 = layout.row()
        row1.operator("pipe.create_project", text="Create Project", icon="WORLD")
        row1.operator("wm.save_userpref", text="Save Project", icon="DOCUMENTS")


# =============== Registration ===============

classes = [
    MyProperties,
    PIPE_OT_create_project,
    PIPE_OT_create_group,
    PIPE_OT_create_asset,
    PIPE_OT_create_shot,
    PIPE_OT_open_asset,
    PIPE_OT_version_up,
    PIPE_OT_publish,
    PIPE_OT_set_output_cg,
    PIPE_OT_apply_render_config,
    PIPE_OT_render_with_prompt,
    PIPE_OT_set_frame_range,
    PIPE_OT_open_publish,
    PIPE_OT_clear_enum,
    PIPE_OT_override_collection,
    preferences_panel,
    VIEW3D_PT_context,
    VIEW3D_PT_assets_shots,
    VIEW3D_PT_settings,
    VIEW3D_PT_publish_browser
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.woody = bpy.props.PointerProperty(type=MyProperties)

    bpy.types.Scene.shot_frame_start = bpy.props.IntProperty(name="Start Frame")
    bpy.types.Scene.shot_frame_end = bpy.props.IntProperty(name="End Frame")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    if hasattr(bpy.types.Scene, "woody"):
        del bpy.types.Scene.woody
    
    if hasattr(bpy.types.Scene, "shot_frame_start"):
        del bpy.types.Scene.shot_frame_start
    if hasattr(bpy.types.Scene, "shot_frame_end"):
        del bpy.types.Scene.shot_frame_end

if __name__ == "__main__":
    register()
