from ..utils.context import context_names

import bpy

class VIEW3D_PT_context(bpy.types.Panel):
     
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Context"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout

        root, group, asset, type_ = context_names()
         
        rootBox = layout.box()
        rootBox.label(text=f"root - {root}", icon="OUTLINER")
        rootBox.scale_y = 0.75

        groupBox = layout.box()
        groupBox.label(text=f"group - {group}", icon="GROUP_VERTEX")
        groupBox.scale_y = 0.75

        assetBox = layout.box()
        assetBox.label(text=f"asset - {asset}", icon="MESH_CUBE")
        assetBox.scale_y = 0.75

        typeBox = layout.box()
        typeBox.label(text=f"type - {type_}", icon="OUTLINER_DATA_POINTCLOUD")
        typeBox.scale_y = 0.75