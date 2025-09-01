import bpy

class PIPE_OT_clear_enum(bpy.types.Operator):
    bl_idname = "pipe.clear_enum"
    bl_label = "Clear Selection"
    bl_description = "Reset this field to 'None'"

    prop_name: bpy.props.StringProperty()# type:ignore

    def execute(self, context):
        setattr(context.scene.woody, self.prop_name, "NONE")
        return {'FINISHED'}

def unlink_collection_from_scene(col, parent=None):
    """Recursively unlink a collection from the scene hierarchy if present."""
    if parent is None:
        parent = bpy.context.scene.collection

    if col in parent.children.values():
        parent.children.unlink(col)
        return True  # ✅ stop after unlinking

    for child in parent.children:
        if unlink_collection_from_scene(col, child):
            return True

    return False