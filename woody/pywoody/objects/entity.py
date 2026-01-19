from ..core.database import get_db
from ..core.directory import Directory
from ..core.console import WoodyError, woody_logger, SUCCESS_LEVEL 
from .guard import Guard
from datetime import datetime

class Entity():
    guard = Guard()
    
    def __init__(self, entity_type: str, project_name: str, collection: str, name: str, woody_id: str):
        self.db = get_db()
        if not self.db: raise RuntimeError("Database not initialized")
        
        self.entity_type = entity_type
        self.project_name = project_name
        self.collection = collection
        self.name = name
        self.woody_id = woody_id

    def _execute(self, task, error_prefix="Operation"):
        self.db.use(self.project_name, self.collection)
        result = self.db.run(task)
        
        if isinstance(result, dict) and result.get("status") == "error":
            msg = result.get('message', '')
            if "duplicate" in msg.lower():
                raise WoodyError(f"{self.entity_type} '{self.name}' already exists.", label="Warning", level="warning")
            raise WoodyError(f"{error_prefix} failed: {msg}")
            
        if not result:
            raise WoodyError(f"{error_prefix} failed: No result from database.")
        return result

    def create(self, data: dict, folder_structure: dict):
        self.db.run(self.db.ensure_unique("woody_id"))
        
        merged_data = {
            "woody_id": self.woody_id,
            "name": self.name, 
            **data,
            "created_by": self.guard._preferences.get("user"),
            "modified_time": datetime.now().isoformat(),
            "created_time": datetime.now().isoformat(), 
            "status": "active"
        }
        
        self._execute(self.db.save_one(merged_data), "Creation")
        
        Directory().create(folder_structure)

        msg = f"{self.entity_type} '{self.name}' created successfully"
        woody_logger.log(SUCCESS_LEVEL, msg)
        
        return msg
    
    def update(self, data: dict):
        query = {"woody_id": self.woody_id}
        merged_data = {
            **data,
            "modified_time": datetime.now().isoformat(),
        }
        
        self._execute(self.db.update(query, merged_data), "Update")
        
        msg = f"{self.entity_type} '{self.name or 'Entity'}' updated successfully."
        woody_logger.log(SUCCESS_LEVEL, msg)
        
        return msg
    
    def archive(self):
        query = {"woody_id": self.woody_id}
        data = {
            "status": "archived",
            "modified_time": datetime.now().isoformat(),
            }
        
        self._execute(self.db.update(query, data), "Archive")
        
        msg = f"{self.entity_type} '{self.name}' archived successfully."
        woody_logger.log(SUCCESS_LEVEL, msg)
        
        return msg