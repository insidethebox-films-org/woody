import tempfile

def generate_config_script(config_path):
    # Create a temp script that runs inside Blender
    script = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w")
    script.write(f"""
import bpy
import json

with open(r"{config_path}", "r") as f:
    config = json.load(f)

bpy.context.scene.frame_start = config.get("frame_start", 1)
bpy.context.scene.frame_end = config.get("frame_end", 250)
print(f"[generate_config_script] ✅ Frame range set from config: {{bpy.context.scene.frame_start}} to {{bpy.context.scene.frame_end}}")
""")
    script.close()
    return script.name