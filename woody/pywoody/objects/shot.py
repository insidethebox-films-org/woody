from .entity import Entity
from .woody_id import WoodyID
from .guard import Guard

class Shot():
    guard = Guard()
    
    def __init__(self, group: str = None, shot_name: str = None):
        self.entity_type = "Shot"
        self.collection = "shots"
        
        self.project_name = self.guard._current_project
        self.tree = "shots"
        self.group = group or self.guard._context[1]
        self.shot_name = shot_name or self.guard._context[2]
        
        self.woody_id = WoodyID().create(
            self.project_name, 
            [self.tree, self.group, self.shot_name]
        )
            
        self.entity = Entity(
            entity_type=self.entity_type,
            project_name=self.project_name,
            collection=self.collection,
            name=self.shot_name,
            woody_id=self.woody_id
        )

    def create(self, start_frame=1001, end_frame=1100):
        
        data = {
            "sequence": self.group,
            "name": self.shot_name,
            "versions": {},
            "frame_range": {
                "start_frame": start_frame,
                "end_frame": end_frame
            }
            
        }
        
        folder_structure = {
            self.project_name: {
                self.tree: {
                    self.group: {
                        self.shot_name: {}
                    }    
                }, 
            }
        }
        
        return self.entity.create(data, folder_structure)

    def update(self, data: dict):
        return self.entity.update(data)
    
    def archive(self):
        return self.entity.archive()