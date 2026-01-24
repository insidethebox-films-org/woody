from ..core.console import woody_logger, SUCCESS_LEVEL
from .entity import Entity
from .woody_id import WoodyID
from .guard import Guard

class Publish():
    guard = Guard()
    
    def __init__(self, publish_name: str = None, type: str = None):
        if self.guard._context == None:
            msg = "Please select a vaild context to create/modify publishes."
            return woody_logger.warning(msg)
        
        self.entity_type = "Publish"
        self.collection = "publishes"
        
        self.project_name = self.guard._current_project
        self.tree = self.guard._context[0]
        self.group = self.guard._context[1]
        self.asset_name = self.guard._context[2]
        
        self.product_type = "publishes"
        self.publish_name = publish_name or self.guard._context[4]
        self.type = type
        
        self.woody_id = WoodyID().create(
            self.project_name, 
            [self.tree, self.group, self.asset_name],
            self.product_type, 
            self.publish_name
        )
            
        self.entity = Entity(
            entity_type=self.entity_type,
            project_name=self.project_name,
            collection=self.collection,
            name=self.publish_name,
            woody_id=self.woody_id
        )

    def create(self):
        data = {
            "type": self.type,
            "versions": {}
        }
        
        folder_structure = {
           self.project_name: {
                self.tree: {
                    self.group: {
                        self.asset_name: {
                            self.product_type: {
                                self.type: {
                                    self.publish_name: {} 
                                }
                            }
                        }
                    }    
                }
           }
        }
        
        return self.entity.create(data, folder_structure)

    def update(self, data: dict):
        return self.entity.update({"woody_id": self.woody_id}, data)
    
    def archive(self):
        return self.entity.archive()