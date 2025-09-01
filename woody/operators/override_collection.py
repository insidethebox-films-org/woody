import bpy

class PIPE_OT_override_collection(bpy.types.Operator):
    bl_idname = "pipe.override_collection"
    bl_label = "Override Linked Collection"
    bl_description = "Create a full library override (content) for the specified linked collection"

    collection_name: bpy.props.StringProperty()# type:ignore
    
    def unlink_collection_from_scene(self, col, parent=None):
        """Recursively unlink a collection from the scene hierarchy if present."""
        if parent is None:
            parent = bpy.context.scene.collection

        if col in parent.children.values():
            parent.children.unlink(col)
            return True  # ✅ stop after unlinking

        for child in parent.children:
            if self.unlink_collection_from_scene(col, child):
                return True

        return False

    def execute(self, context):
        col = bpy.data.collections.get(self.collection_name)
        if not col:
            self.report({'ERROR'}, f"Collection '{self.collection_name}' not found.")
            return {'CANCELLED'}

        if col.override_library:
            self.report({'INFO'}, f"Collection '{col.name}' is already overridden.")
            return {'CANCELLED'}

        try:
            override = col.override_hierarchy_create(
                scene=context.scene,
                view_layer=context.view_layer,
                do_fully_editable=True
            )

            # ✅ Unlink the original linked collection (works at any depth)
            if self.unlink_collection_from_scene(col):
                self.report({'INFO'}, f"Unlinked original linked collection: {col.name}")
            else:
                self.report({'WARNING'}, f"Could not unlink {col.name} (was not in scene hierarchy).")

            self.report({'INFO'}, f"Full override created for: {override.name}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Override failed: {e}")
            return {'CANCELLED'}