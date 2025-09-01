from ..preferences import *

import bpy
from pathlib import Path

class VIEW3D_PT_publish_browser(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Woody Asset Browser"
    bl_category = "WoodyAssetBrowser"
    
    def is_collection_linked_and_not_overridden(self, col):
        """Return True if collection is linked directly (from _published.blend), in scene, and not overridden."""
        if not col.library:
            return False
        if not self.collection_in_scene(col):  # ✅ works at any depth
            return False
        for other in bpy.data.collections:
            if other.override_library and other.override_library.reference == col:
                return False
        return "_published.blend" in col.library.filepath

    def is_collection_override_of_published(self, col):
        """Return True if collection is an override of a published link in the scene."""
        if not col.override_library:
            return False

        if not self.collection_in_scene(col):  # ✅ works at any depth
            return False

        ref = col.override_library.reference
        if not ref or not ref.library:
            return False

        return "_published.blend" in ref.library.filepath

    def is_published_file_already_in_scene(self, blend_path):
        for c in bpy.data.collections:
            if c.library and c.library.filepath == blend_path and not c.override_library:
                if self.collection_in_scene(c):
                    return True
            if c.override_library:
                ref = c.override_library.reference
                if ref and ref.library and ref.library.filepath == blend_path:
                    if self.collection_in_scene(c):
                        return True
        return False

    def collection_in_scene(self, col, parent=None):
        """Check if a collection is in the scene hierarchy (at any depth)."""
        if parent is None:
            parent = bpy.context.scene.collection

        if col == parent:
            return True

        for child in parent.children:
            if self.collection_in_scene(col, child):
                return True

        return False

    def walk_children(self, col, collected=None):
        """Recursively gather all child collections of a given collection."""
        if collected is None:
            collected = set()
        for child in col.children:
            collected.add(child)
            self.walk_children(child, collected)
        return collected

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.woody

        def draw_enum_with_clear(layout, prop_id, label=""):
            row = layout.row(align=True)
            row.prop(props, prop_id, text=label)
            op = row.operator("pipe.clear_enum", text="", icon="X")
            op.prop_name = prop_id

        draw_enum_with_clear(layout, "root_folder", "Root")
        draw_enum_with_clear(layout, "group_folder", "Group")
        draw_enum_with_clear(layout, "asset_folder", "Asset")

        layout.separator()
        layout.label(text="Published Files:")

        box = layout.box()
        col = box.column()
        col.scale_y = 0.95

        base_path = Path(bpy.path.abspath(get_directory()))
        if props.root_folder and props.root_folder != "NONE":
            base_path /= props.root_folder
            if props.group_folder and props.group_folder != "NONE":
                base_path /= props.group_folder
                if props.asset_folder and props.asset_folder != "NONE":
                    base_path /= props.asset_folder
        if not base_path.exists():
            layout.label(text="Invalid path.", icon="ERROR")
            return

        blend_files = list(base_path.rglob("*_published.blend"))

        if blend_files:
            for blend_file in blend_files:
                row = col.row(align=True)
                row.label(text=blend_file.name, icon="FILE_BLEND")

                # Get the relative blend path to match against linked/overridden collections
                blend_path_str = str(blend_file)

                # Check if already linked or overridden
                if not self.is_published_file_already_in_scene(blend_path_str):
                    op = row.operator("pipe.open_publish", text="", icon="IMPORT")
                    op.filepath = blend_path_str
                else:
                    row.label(icon="CHECKMARK")
        else:
            layout.label(text="No published files found.", icon="INFO")


        layout.separator()
        layout.label(text="Linked Published Collections:")
        box = layout.box()
        col = box.column()

        linked_collections = [c for c in bpy.data.collections if self.is_collection_linked_and_not_overridden(c)]

        # Remove subcollections of already-linked collections
        excluded = set()
        for c in linked_collections:
            excluded.update(self.walk_children(c))
        linked_collections = [c for c in linked_collections if c not in excluded]

        if linked_collections:
            for col_item in linked_collections:
                row = col.row(align=True)
                row.label(text=col_item.name, icon="OUTLINER_COLLECTION")
                op = row.operator("pipe.override_collection", text="", icon="IMPORT")
                op.collection_name = col_item.name
        else:
            col.label(text="No linked published collections.")

        layout.separator()
        layout.label(text="Overridden Published Collections:")
        box = layout.box()
        col = box.column()

        overridden_collections = [c for c in bpy.data.collections if self.is_collection_override_of_published(c)]

        # Remove subcollections of already-overridden collections
        excluded = set()
        for c in overridden_collections:
            excluded.update(self.walk_children(c))
        overridden_collections = [c for c in overridden_collections if c not in excluded]

        if overridden_collections:
            for col_item in overridden_collections:
                row = col.row(align=True)
                row.label(text=col_item.name, icon="LIBRARY_DATA_OVERRIDE")
        else:
            col.label(text="No overridden published collections.")