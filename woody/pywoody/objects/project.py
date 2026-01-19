from .entity import Entity
from .woody_id import WoodyID
from .guard import Guard

class Project():
    guard = Guard()
    
    def __init__(self, project_name: str = None):
        self.entity_type = "Project"
        self.collection = "project"
        
        self.project_name = project_name or self.guard._current_project
        
        if self.project_name:
            self.woody_id = WoodyID().create(self.project_name)
            
            self.entity = Entity(
                entity_type=self.entity_type,
                project_name=self.project_name,
                collection=self.collection,
                name=self.project_name,
                woody_id=self.woody_id  
            )

    @classmethod
    def create(cls, project_name: str):
        new_project = cls(project_name)
        
        data = {
            "project_path": f"{cls.guard._preferences.get('projects_directory')}\\{project_name}"
        }
        
        folder_structure = {
            project_name: {"assets": {}, "shots": {}}
        }
        
        new_project.entity.create(data, folder_structure)
        
        cls.guard.set_current_project(project_name)
        
        return f"Project {project_name} is now active."

    def update(self, data: dict):
        return self.entity.update(data)
    
    def archive(self):
        return self.entity.archive()