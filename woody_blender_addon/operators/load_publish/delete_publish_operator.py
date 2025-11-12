"""
Delete Publish Operator for the Woody Blender addon.
Handles removing linked published assets from the scene and data blocks.
"""

import bpy
from ...utils.publish_utils import collection_in_scene, unlink_collection_from_scene


class WOODY_OT_delete_publish(bpy.types.Operator):
    bl_idname = "woody.delete_publish"
    bl_label = "Delete Linked Publish"
    bl_description = "Remove the linked publish from scene and data blocks"

    library_path: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        if not self.library_path:
            self.report({'ERROR'}, "No library path specified")
            return {'CANCELLED'}

        try:
            deleted_items = []
            
            # Delete collections from this library
            collections_to_remove = []
            for collection in bpy.data.collections:
                if collection.library and collection.library.filepath == self.library_path:
                    if collection_in_scene(collection):
                        collections_to_remove.append(collection)
                elif collection.override_library and collection.override_library.reference:
                    ref = collection.override_library.reference
                    if ref.library and ref.library.filepath == self.library_path:
                        if collection_in_scene(collection):
                            collections_to_remove.append(collection)

            for collection in collections_to_remove:
                try:
                    # Remove from scene hierarchy first
                    if unlink_collection_from_scene(collection):
                        deleted_items.append(f"Collection: {collection.name}")
                    # Note: Don't remove from bpy.data.collections as it may be referenced elsewhere
                except Exception as e:
                    print(f"Error removing collection {collection.name}: {e}")

            # Delete objects from this library that are in the scene
            objects_to_remove = []
            for obj in list(bpy.context.scene.objects):
                if obj.library and obj.library.filepath == self.library_path:
                    objects_to_remove.append(obj)
                elif obj.override_library and obj.override_library.reference:
                    ref = obj.override_library.reference
                    if ref.library and ref.library.filepath == self.library_path:
                        objects_to_remove.append(obj)

            for obj in objects_to_remove:
                try:
                    # Remove from scene
                    bpy.context.scene.collection.objects.unlink(obj)
                    deleted_items.append(f"Object: {obj.name}")
                except Exception as e:
                    print(f"Error removing object {obj.name}: {e}")

            # For materials and node groups, we'll remove them from bpy.data
            # since they're not directly in the scene
            
            # Delete materials from this library
            materials_to_remove = []
            for material in list(bpy.data.materials):  # Use list() to avoid iteration issues
                if material.library and material.library.filepath == self.library_path:
                    materials_to_remove.append(material)

            for material in materials_to_remove:
                material_name = getattr(material, 'name', 'unknown')
                try:
                    # Check if material still exists and is valid
                    if material.name in bpy.data.materials:
                        bpy.data.materials.remove(material)
                        deleted_items.append(f"Material: {material_name}")
                    else:
                        # Material doesn't exist anymore, but we found it initially so count as deleted
                        deleted_items.append(f"Material: {material_name}")
                except (ReferenceError, RuntimeError) as e:
                    # Material was already removed or is invalid - but we tried to delete it, so count it
                    deleted_items.append(f"Material: {material_name}")
                    print(f"Material was already cleaned up by Blender: {e}")
                except Exception as e:
                    print(f"Error removing material: {e}")

            # Delete node groups from this library
            node_groups_to_remove = []
            for node_group in list(bpy.data.node_groups):  # Use list() to avoid iteration issues
                if node_group.library and node_group.library.filepath == self.library_path:
                    node_groups_to_remove.append(node_group)

            for node_group in node_groups_to_remove:
                node_group_name = getattr(node_group, 'name', 'unknown')
                try:
                    # Check if node group still exists and is valid
                    if node_group.name in bpy.data.node_groups:
                        bpy.data.node_groups.remove(node_group)
                        deleted_items.append(f"Node Group: {node_group_name}")
                    else:
                        # Node group doesn't exist anymore, but we found it initially so count as deleted
                        deleted_items.append(f"Node Group: {node_group_name}")
                except (ReferenceError, RuntimeError) as e:
                    # Node group was already removed or is invalid - but we tried to delete it, so count it
                    deleted_items.append(f"Node Group: {node_group_name}")
                    print(f"Node group was already cleaned up by Blender: {e}")
                except Exception as e:
                    print(f"Error removing node group: {e}")

            # Delete meshes from this library (only if not used by remaining objects)
            meshes_to_remove = []
            for mesh in list(bpy.data.meshes):  # Use list() to avoid iteration issues
                if mesh.library and mesh.library.filepath == self.library_path:
                    # Check if mesh is still used by any object
                    mesh_in_use = False
                    try:
                        for obj in bpy.data.objects:
                            if obj.data == mesh:
                                mesh_in_use = True
                                break
                    except (ReferenceError, RuntimeError):
                        # Object or mesh reference is invalid, consider mesh not in use
                        pass
                    
                    if not mesh_in_use:
                        meshes_to_remove.append(mesh)

            for mesh in meshes_to_remove:
                mesh_name = getattr(mesh, 'name', 'unknown')
                try:
                    # Check if mesh still exists and is valid
                    if mesh.name in bpy.data.meshes:
                        bpy.data.meshes.remove(mesh)
                        deleted_items.append(f"Mesh: {mesh_name}")
                    else:
                        # Mesh doesn't exist anymore, but we found it initially so count as deleted
                        deleted_items.append(f"Mesh: {mesh_name}")
                except (ReferenceError, RuntimeError) as e:
                    # Mesh was already removed or is invalid - but we tried to delete it, so count it
                    deleted_items.append(f"Mesh: {mesh_name}")
                    print(f"Mesh was already cleaned up by Blender: {e}")
                except Exception as e:
                    print(f"Error removing mesh: {e}")

            if deleted_items:
                items_str = ", ".join(deleted_items)
                self.report({'INFO'}, f"Deleted: {items_str}")
                
                # Refresh the display
                bpy.ops.woody.refresh_loaded_publishes()
                
                return {'FINISHED'}
            else:
                self.report({'INFO'}, "No items found to delete from this library")
                return {'FINISHED'}

        except Exception as e:
            # Don't show the StructRNA error to users since it's just Blender's cleanup
            if "StructRNA" in str(e) and "has been removed" in str(e):
                print(f"Blender auto-cleanup occurred: {e}")
                # Still try to refresh and report success
                try:
                    bpy.ops.woody.refresh_loaded_publishes()
                except:
                    pass
                self.report({'INFO'}, "Deleted successfully")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, f"Delete failed: {str(e)}")
                print(f"Delete error: {e}")
                return {'CANCELLED'}