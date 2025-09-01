import bpy

def get_preferences():
    try:
        return bpy.context.preferences.addons["woody"].preferences
    except KeyError:
        return None

def get_directory():
    prefs = get_preferences()
    return prefs.directory if prefs else ""

def get_blender_version():
    prefs = get_preferences()
    return prefs.blenderVersion if prefs else ""

class preferences(bpy.types.AddonPreferences):
    bl_idname = "woody"
    
    directory: bpy.props.StringProperty(
        name="Directory",
        subtype='DIR_PATH',
        description="Root directory for all projects"
    ) # type: ignore
    blenderVersion: bpy.props.StringProperty(
        name="EXE Path",
        subtype='FILE_PATH',
        description="Path to your blender.exe"
    ) # type: ignore
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_props = scene.woody

        pathsBox = layout.box()
        pathsBox.label(text="Paths")
        pathsBox.scale_y = 0.65
        layout.prop(self, "directory")
        layout.prop(self, "blenderVersion")

        projectBox = layout.box()
        projectBox.label(text="Project")
        projectBox.scale_y = 0.65

        row1 = layout.row()
        row1.operator("pipe.create_project", text="Create Project", icon="WORLD")
        row1.operator("wm.save_userpref", text="Save Project", icon="DOCUMENTS")