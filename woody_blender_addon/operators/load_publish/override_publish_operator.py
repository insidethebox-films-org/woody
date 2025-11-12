"""
Override Publish Operator for the Woody Blender addon.
Handles creating library overrides for linked published assets.
"""

import bpy
from ...utils.publish_utils import collection_in_scene, unlink_collection_from_scene


class WOODY_OT_override_publish(bpy.types.Operator):
    bl_idname = "woody.override_publish"
    bl_label = "Override Linked Publish"
    bl_description = "Create a library override for the linked publish while maintaining update capability"

    library_path: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        if not self.library_path:
            self.report({'ERROR'}, "No library path specified")
            return {'CANCELLED'}

        try:
            # Check if this library is already fully overridden
            all_overridden = True
            has_any_assets = False
            
            # Check collections
            for col in bpy.data.collections:
                if col.library and col.library.filepath == self.library_path:
                    has_any_assets = True
                    if collection_in_scene(col):
                        if not col.override_library:
                            all_overridden = False
                            break
            
            # Check objects if no collections found
            if not has_any_assets:
                for obj in bpy.data.objects:
                    if obj.library and obj.library.filepath == self.library_path:
                        has_any_assets = True
                        try:
                            # Check if object is in scene collection using proper method
                            if obj.name in context.scene.collection.objects:
                                if not obj.override_library:
                                    all_overridden = False
                                    break
                        except (TypeError, AttributeError):
                            continue
            
            if not has_any_assets:
                self.report({'INFO'}, "No assets from this library found in scene")
                return {'FINISHED'}
                
            if all_overridden:
                self.report({'INFO'}, "All assets from this library are already overridden")
                return {'FINISHED'}

            # Find collections from this library that are in the scene
            scene_collections = []
            for col in bpy.data.collections:
                if (col.library and 
                    col.library.filepath == self.library_path and 
                    collection_in_scene(col) and
                    not col.override_library):  # Only non-overridden collections
                    scene_collections.append(col)

            if not scene_collections:
                # Check for objects not in collections
                scene_objects = []
                for obj in bpy.data.objects:
                    if (obj.library and 
                        obj.library.filepath == self.library_path and 
                        not obj.override_library):
                        # Check if object is in scene collection using name comparison
                        try:
                            if obj.name in context.scene.collection.objects:
                                scene_objects.append(obj)
                        except (TypeError, AttributeError):
                            # Skip objects that can't be checked properly
                            continue
                
                if not scene_objects:
                    self.report({'INFO'}, "No linked assets from this library found in scene or already overridden")
                    return {'FINISHED'}

            overridden_items = []

            # Override collections
            for col in scene_collections:
                try:
                    # Create override
                    override = col.override_hierarchy_create(
                        scene=context.scene,
                        view_layer=context.view_layer,
                        do_fully_editable=True
                    )
                    
                    if override:
                        # Unlink the original linked collection
                        if unlink_collection_from_scene(col):
                            print(f"Unlinked original collection: {col.name}")
                        else:
                            print(f"Warning: Could not unlink {col.name} from scene")
                        
                        overridden_items.append(f"Collection: {override.name}")
                        
                except Exception as e:
                    self.report({'ERROR'}, f"Failed to override collection {col.name}: {str(e)}")
                    print(f"Override error for {col.name}: {e}")
                    return {'CANCELLED'}

            # Override standalone objects
            for obj in scene_objects if 'scene_objects' in locals() else []:
                try:
                    override = obj.override_hierarchy_create(
                        scene=context.scene,
                        view_layer=context.view_layer,
                        do_fully_editable=True
                    )
                    
                    if override:
                        # Remove original object from scene
                        try:
                            if obj.name in context.scene.collection.objects:
                                context.scene.collection.objects.unlink(obj)
                        except (TypeError, AttributeError):
                            # Object might not be in collection or already removed
                            pass
                        overridden_items.append(f"Object: {override.name}")
                        
                except Exception as e:
                    self.report({'ERROR'}, f"Failed to override object {obj.name}: {str(e)}")
                    print(f"Override error for {obj.name}: {e}")
                    return {'CANCELLED'}

            if overridden_items:
                items_str = ", ".join(overridden_items)
                self.report({'INFO'}, f"✅ Created overrides: {items_str}")
                
                # Refresh the display by calling the refresh operator
                bpy.ops.woody.refresh_loaded_publishes()
                
                return {'FINISHED'}
            else:
                self.report({'INFO'}, "No items were overridden")
                return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Override failed: {str(e)}")
            print(f"General override error: {e}")
            return {'CANCELLED'}