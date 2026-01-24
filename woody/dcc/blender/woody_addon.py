import bpy
from woody.pywoody.handlers.processor import Processor

bl_info = {
    "name": "Woody",
    "author": "Woody Team",
    "version": (1, 0, 0),
    "blender": (5, 0, 1),
    "location": "View3D > Sidebar > Woody",
    "description": "Woody Pipeline Integration",
    "category": "Pipeline",
}

class WOODY_PT_MainPanel(bpy.types.Panel):
    """Woody Main Panel"""
    bl_label = "Woody"
    bl_idname = "WOODY_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Woody'

    def draw(self, context):
        layout = self.layout
        layout.operator("woody.test_button")


class WOODY_OT_TestButton(bpy.types.Operator):
    """temp operator"""
    bl_label = "Print Hello"
    bl_idname = "woody.test_button"

    def execute(self, context):
        print("Hello")
        Processor().list_projects()
        self.report({'INFO'}, "Hello")
        return {'FINISHED'}


classes = (
    WOODY_PT_MainPanel,
    WOODY_OT_TestButton,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
