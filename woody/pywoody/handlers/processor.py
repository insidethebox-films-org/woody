from ..core.console import handle_woody_errors, woody_logger, SUCCESS_LEVEL
from ..core.queries import Queries
from ..objects.preferences import Preferences
from ..objects.guard import Guard
from ..objects.context import Context
from ..objects.project import Project
from ..objects.asset import Asset
from ..objects.shot import Shot
from ..objects.scene import Scene
from ..objects.publish import Publish
from woody.dcc.blender.blender import Blender

class Processor:
    guard = Guard()
    
    # ------- Context ------- #
    
    @handle_woody_errors
    def set_context(self, value):
        context = Context()
        return context.set(value)
        
    @handle_woody_errors
    def get_context(self):
        context = Context()
        return context.get()
    
    @handle_woody_errors
    def clear_context(self):
        self.guard.clear_context()
    
    # ------- List ------- #
    
    @handle_woody_errors
    def list_projects(self):
        query = Queries()
        return query.list_projects()
    
    @handle_woody_errors
    def list_groups(self, tree: str = None):
        tree = tree or self.guard._context.get("tree")
        
        query = Queries()
        return query.list_groups(tree)
    
    @handle_woody_errors
    def list_names(self, tree: str = None, group: str = None):
        tree = tree or self.guard._context.get("tree")
        group = group or self.guard._context.get("group")
        
        query = Queries()
        return query.list_names(tree, group)
    
    # ------- Project ------- #
    
    @handle_woody_errors
    def switch_projects(self, project_name: str):
        prefs = Preferences()
        return prefs.switch_projects(project_name)
    
    @handle_woody_errors
    def create_project(self, project_name: str):
        prefs = Preferences()
        project = Project()
        
        return project.create(project_name), prefs.switch_projects(project_name)
    
    @handle_woody_errors
    def update_project(self, data):
        project = Project()
        return project.update(data)
    
    # ------- Asset ------- #
    
    @handle_woody_errors
    def create_asset(self, group: str, asset_name: str):
        asset = Asset(group, asset_name)
        context = Context("assets", group, asset_name)
        
        return asset.create(), context.set()
    
    @handle_woody_errors
    def update_asset(self, data):
        asset = Asset()
        return asset.update(data)
    
    # ------- Shot ------- #
    
    @handle_woody_errors
    def create_shot(self, group, shot_name, start_frame=None, end_frame=None):
        shot = Shot(group, shot_name)
        context = Context("shots", group, shot_name)
        
        return shot.create(start_frame, end_frame), context.set()

    # ------- Scene ------- #
    
    @handle_woody_errors
    def create_scene(self, scene_name, dcc):  
        scene = Scene(scene_name, dcc)
        context = Context(
            self.guard._context.get("tree"),
            self.guard._context.get("group"),
            self.guard._context.get("asset"),
            "scenes",
            scene_name
        )
        
        return scene.create(), context.set()
    
    # ------- Publish ------- #

    @handle_woody_errors
    def create_publish(self, publish_name, publish_type):  
        publish = Publish(publish_name, publish_type)

        return publish.create()
    
    # ------- Blender ------- #
    
    @handle_woody_errors
    def install_blender(self, exe, force_update=None):
        blender = Blender()
        return blender.install(exe, force_update)
    
    @handle_woody_errors
    def uninstall_blender(self):
        blender = Blender()
        return blender.uninstall()
    
    def launch_blender(self):
        blender = Blender()
        return blender.launch()
    