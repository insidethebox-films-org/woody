from ..core.console import handle_woody_errors
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
    def set_context(self, tree, group, asset, product_type = None, product_name = None):
        context = Context(tree, group, asset, product_type, product_name)
        return context.set_context()
    
    # ------- List ------- #
    
    @handle_woody_errors
    def list_projects(self):
        query = Queries()
        return query.list_projects()
    
    @handle_woody_errors
    def list_groups(self, tree):
        query = Queries()
        return query.list_groups(tree)
    
    @handle_woody_errors
    def list_names(self, tree, group):
        query = Queries()
        return query.list_names(tree, group)
    
    # ------- Project ------- #
    
    @handle_woody_errors
    def switch_projects(self, project_name):
        prefs = Preferences()
        return prefs.switch_projects(project_name)
    
    @handle_woody_errors
    def create_project(self, project_name):
        prefs = Preferences()
        project = Project()
        
        return project.create(project_name), prefs.switch_projects(project_name)
    
    @handle_woody_errors
    def update_project(self, data):
        project = Project()
        return project.update(data)
    
    # ------- Asset ------- #
    
    @handle_woody_errors
    def create_asset(self, group, asset_name):
        asset = Asset(group, asset_name)
        context = Context("assets", group, asset_name)
        
        return asset.create(), context.set_context()
    
    @handle_woody_errors
    def update_asset(self, data):
        asset = Asset()
        return asset.update(data)
    
    # ------- Shot ------- #
    
    @handle_woody_errors
    def create_shot(self, group, shot_name, start_frame=None, end_frame=None):
        shot = Shot(group, shot_name)
        context = Context("shots", group, shot_name)
        
        return shot.create(start_frame, end_frame), context.set_context()

    # ------- Scene ------- #
    
    @handle_woody_errors
    def create_scene(self, scene_name, dcc):  
        scene = Scene(scene_name, dcc)
        context = Context(
            self.guard._context[0],
            self.guard._context[1],
            self.guard._context[2],
            "scenes",
            scene_name
        )
        
        return scene.create(), context.set_context()

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
    