import bpy
from pathlib import Path

class PIPE_OT_open_publish(bpy.types.Operator):
    bl_idname = "pipe.open_publish"
    bl_label = "Open Publish"
    bl_description = "Link the first collection from a published .blend file into the current scene"

    filepath: bpy.props.StringProperty()# type:ignore

    def execute(self, context):
        blend_path = Path(self.filepath).resolve()
        current_path = Path(bpy.data.filepath).resolve()

        # Extract root/group/asset from both paths
        try:
            def extract_asset_path_parts(path):
                path = Path(path)
                filename = path.stem  # e.g. "lupinPub_model_published"
                
                # Assuming the format is always: asset_type_status
                filename_parts = filename.split("_")
                if len(filename_parts) < 3:
                    raise ValueError(f"Unexpected filename format: {filename}")
                
                asset = filename_parts[0]
                type_ = filename_parts[1]
                
                parts = path.parts
                if len(parts) < 5:
                    return None
                group = parts[-4]
                root = parts[-5]
                
                return root, group, asset, type_

            current_parts = extract_asset_path_parts(current_path)
            target_parts = extract_asset_path_parts(blend_path)

            if current_parts and target_parts and current_parts == target_parts:
                self.report({'ERROR'}, "❌ Cannot link from the same asset you're currently working in.")
                return {'CANCELLED'}

        except Exception as e:
            self.report({'WARNING'}, f"⚠️ Asset path check failed: {e}")
            # Allow linking if check fails

        if not blend_path.exists():
            self.report({'ERROR'}, f"File not found: {blend_path}")
            return {'CANCELLED'}

          # Determine expected collection name
        root, group, asset, type_ = extract_asset_path_parts(blend_path)
        target_collection_name = f"{root}_{group}_{asset}_{type_}"
        print("BLEND PATH: ",blend_path)
        print("TARGET: ",target_collection_name)
        try:
            with bpy.data.libraries.load(str(blend_path), link=True) as (data_from, data_to):
                if target_collection_name not in data_from.collections:
                    self.report({'ERROR'}, f"Expected collection '{target_collection_name}' not found in .blend")
                    return {'CANCELLED'}

                data_to.collections = [target_collection_name]


            linked_col = data_to.collections[0]
            context.scene.collection.children.link(linked_col)

            self.report({'INFO'}, f"✅ Linked collection: {linked_col.name}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Linking failed: {e}")
            return {'CANCELLED'}
