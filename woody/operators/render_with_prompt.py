from ..utils import *

import subprocess
import bpy
from datetime import datetime
from pathlib import Path

class PIPE_OT_render_with_prompt(bpy.types.Operator):
    bl_idname = "pipe.render_with_prompt"
    bl_label = "Render"
    bl_description = "Render animation with version check"

    choice: bpy.props.EnumProperty(
        name="Render Option",
        items=[
            ('OVERWRITE', "Overwrite", "Overwrite existing files"),
            ('NEW_VERSION', "New Version", "Create a new version and render there"),
        ],
        default='OVERWRITE'
    )  # type: ignore
    make_mp4: bpy.props.BoolProperty(
        name="Make Mp4",
        description="Render an mp4 as well.",
        default=False
    )  # type: ignore

    def execute(self, context):
        render_path = Path(bpy.path.abspath(context.scene.render.filepath))

        # Check that we're in a valid asset/shot path
        if not bpy.data.filepath:
            self.report({'ERROR'}, "🚨 File not saved yet.")
            return {'CANCELLED'}

        root, group, asset, type_ = context_names()
        if root not in {"assets", "shots"} or group == "GROUP" or asset == "ASSET":
            self.report({'ERROR'}, f"🚨 Unexpected path: {root}/{group}/{asset}")
            return {'CANCELLED'}

        if self.choice == 'NEW_VERSION':
            success = set_render_output_to_cg()
            if not success:
                self.report({'ERROR'}, "⚠️ Failed to set a new version render path.")
                return {'CANCELLED'}

            render_path = Path(bpy.path.abspath(context.scene.render.filepath))
            self.report({'INFO'}, f"🆕 New version folder set: {render_path}")

        else:
            self.report({'INFO'}, f"📝 Overwriting frames in: {render_path}")
        
        blend_file = bpy.data.filepath 
        bpy.ops.wm.save_mainfile() 
        output_path = Path(bpy.path.abspath(context.scene.render.filepath)) 
        
        subprocess.Popen([ 
            bpy.app.binary_path, 
            "-b", blend_file, 
            "-o", str(output_path / "####"), 
            "-a" 
            ])

        if self.make_mp4:
                version_folder = output_path.name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M")

                mp4_path = output_path.parent / "_mp4" / f"{timestamp}_{version_folder}.mp4"
                mp4_path.parent.mkdir(parents=True, exist_ok=True)

                # Second subprocess → render directly to mp4
                subprocess.Popen([
                    bpy.app.binary_path,
                    "-b", blend_file,
                    "--python-expr", (
                        "import bpy;"
                        "s=bpy.context.scene;"
                        "s.render.image_settings.file_format='FFMPEG';"
                        "s.render.ffmpeg.format='MPEG4';"
                        "s.render.ffmpeg.codec='H264';"
                        "s.render.ffmpeg.constant_rate_factor='HIGH';"
                        "s.render.ffmpeg.ffmpeg_preset='GOOD';"
                        "s.render.filepath=r'{}';"
                        "bpy.ops.render.render(animation=True)".format(mp4_path)
                    )
                ])

        return {'FINISHED'}

    def invoke(self, context, event):
        # Check that we're in a valid asset/shot path
        if not bpy.data.filepath:
            self.report({'ERROR'}, "🚨 File not saved yet.")
            return {'CANCELLED'}

        root, group, asset, type_ = context_names()
        if root not in {"assets", "shots"} or group == "GROUP" or asset == "ASSET":
            self.report({'ERROR'}, f"🚨 Unexpected path: {root}/{group}/{asset}")
            return {'CANCELLED'}

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Render Options:")

        # Get the output folder
        render_path = Path(bpy.path.abspath(context.scene.render.filepath))
        has_existing_frames = any(
            f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.exr', '.blend')
            for f in render_path.iterdir()
            if f.is_file()
        )
        
        if has_existing_frames:
            row = layout.row()
            row.prop(self, "choice", expand=True)

        # Make Mp4 checkbox always visible
        layout.prop(self, "make_mp4")