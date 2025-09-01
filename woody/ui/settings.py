import bpy

class VIEW3D_PT_settings(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Settings"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        frameBox = layout.box()
        frameBox.label(text="Frame Range")
        frameBox.scale_y = 0.65

        

        layout.prop(scene, "shot_frame_start")
        layout.prop(scene, "shot_frame_end")
        layout.operator("pipe.set_frame_range", text="Set Frame Range")