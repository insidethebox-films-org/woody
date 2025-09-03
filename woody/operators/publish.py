from ..lib.blender.get_preferences import get_directory
from ..utils.context import context_names
from ..lib.blender.create_blend_with_collections import create_blend_with_collection
from ..lib.blender.show_popup_message import show_popup_message

import bpy
from pathlib import Path

class PIPE_OT_publish(bpy.types.Operator):
    bl_idname = "pipe.publish"
    bl_label = "Publish"
    bl_description = "Publish the current asset to a dedicated file"

    def invoke(self, context, event):
        # This opens a Blender-native confirmation popup
        return context.window_manager.invoke_confirm(self, event)
    
    def execute(self, context):

        directory = get_directory()
        directory = Path(directory)

        print("DIRECTORY:  ",directory)

        root, group, asset, type_ = context_names()
        collection_name = root + "_" + group + "_" + asset + "_" + type_
        tags = [root, group, asset, type_]

        collection = bpy.data.collections.get(collection_name)

        filePath = directory / root / group / asset / "_publish" 
        print("FILEPATH: ", filePath)

        #export_dir = directory / "_publish"
        export_filename = asset + "_" + type_ + "_published" + ".blend"
        export_path = filePath / export_filename

        print("EXPRTPATH: ", export_path)
        create_blend_with_collection(export_filename, collection_name, filePath)

        # Feedback (status bar + popup)
        self.report({'INFO'}, f"✅ Published to: {export_filename}")
        show_popup_message("✅ Asset has been published!", title="Publish Complete", icon='CHECKMARK')
        
        return {"FINISHED"}