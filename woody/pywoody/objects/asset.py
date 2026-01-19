from .entity import Entity
from .woody_id import WoodyID
from .guard import Guard

class Asset():
    guard = Guard()
    
    def __init__(self, group: str = None, asset_name: str = None):
        self.entity_type = "Asset"
        self.collection = "assets"
        
        self.project_name = self.guard._current_project
        self.tree = "assets"
        self.group = group or self.guard._context[1]
        self.asset_name = asset_name or self.guard._context[2]
        
        self.woody_id = WoodyID().create(
            self.project_name, 
            [self.tree, self.group, self.asset_name]
        )
            
        self.entity = Entity(
            entity_type=self.entity_type,
            project_name=self.project_name,
            collection=self.collection,
            name=self.asset_name,
            woody_id=self.woody_id
        )

    def create(self):
        
        data = {
            "group": self.group,
            "name": self.asset_name,
            "versions": {}
        }
        
        folder_structure = {
            self.project_name: {
                self.tree: {
                    self.group: {
                        self.asset_name: {}
                    }    
                }, 
            }
        }
        
        return self.entity.create(data, folder_structure)

    def update(self, data: dict):
        return self.entity.update(data)
    
    def archive(self):
        return self.entity.archive()