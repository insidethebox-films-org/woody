import bpy

class VIEW3D_PT_assets_shots(bpy.types.Panel):
     
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Assets/Shots"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout

        newAssetBox = layout.box()
        newAssetBox.label(text="New")
        newAssetBox.scale_y = 0.65

        layout.operator("pipe.create_group", text="New Group", icon="GROUP_VERTEX")

        row1 = self.layout.row()
        row1.operator("pipe.create_asset", text="New Asset", icon="OUTLINER_OB_META")
        row1.operator("pipe.create_shot", text="New Shot", icon="VIEW_CAMERA")

        fileBox = layout.box()
        fileBox.label(text="File")
        fileBox.scale_y = 0.65

        row2 = self.layout.row()
        row2.operator("pipe.open_asset", text="Open", icon="COPY_ID")
        row2.operator("pipe.save_asset", text="Save", icon="NODE_COMPOSITING")
        
        publishBox = layout.box()
        publishBox.label(text="Publish")
        publishBox.scale_y = 0.65
        
        row3 = layout.row()
        row3.operator("pipe.publish", text="Publish", icon="DISK_DRIVE")
        
        renderBox = layout.box()
        renderBox.label(text="Render")
        renderBox.scale_y = 0.65

        row4 = layout.row()
        row4.operator("pipe.set_output_cg", text="Set Render Path", icon="RENDER_STILL")
        row4.operator("pipe.apply_render_config", text="Set Configs", icon="PREFERENCES")
        
        layout.operator("pipe.render_with_prompt", text="Render", icon="RENDER_ANIMATION")