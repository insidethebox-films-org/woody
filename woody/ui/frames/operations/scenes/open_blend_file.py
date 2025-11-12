from .....tool.woody_instance import WoodyInstance
from .....plugins.blender.blender_instance import BlenderInstance

def open_blend_file(blends_list_box, blend_version_list_box):
    
    woody = WoodyInstance().browser_selection()
    blender = BlenderInstance()
    group_type_selection = woody.get("group_type")
    group_selection = woody.get("group")
    element_selection = woody.get("element")
    blend_selection = blends_list_box.get()
    version_selection = blend_version_list_box.get()
    
    group_type = "assets" if group_type_selection == "Assets Group" else "shots"
    
    if not version_selection == "latest":
        v = "v"
    else:
        v = ""
    
    blender.open_file(
        group_type,
        group_selection, 
        element_selection,
        f"{blend_selection}_{v}{version_selection}.blend",
    )   
