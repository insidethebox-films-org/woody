import bpy

def save_current_scene():

    if bpy.data.filepath:
        bpy.ops.wm.save_mainfile()
        print(f"Scene saved: {bpy.data.filepath}")
    else:
        print("Scene has not been saved before. Skipping save.")