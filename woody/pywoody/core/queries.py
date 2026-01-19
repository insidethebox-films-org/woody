from .database import get_db
from ..objects.guard import Guard
from ..core.console import WoodyError, woody_logger, SUCCESS_LEVEL 

class Queries():
    guard = Guard()
    
    def __init__(self):
        self.db = get_db()
        if not self.db: 
            raise WoodyError("Database not initialized", level="error")
        
    def list_projects(self):
        self.db.use(self.guard._current_project)
        projects = self.db.run(self.db.list_projects())
        
        sorted_projects = sorted(projects)
        
        project_list = '\n'.join(f"  - {project}" for project in sorted_projects)
        msg = f"Available Projects:\n{project_list}"
        woody_logger.log(SUCCESS_LEVEL, msg)
        
        return sorted(projects)
        
    def list_groups(self, tree):
        if not self.db or not self.guard._current_project:
            woody_logger.log(SUCCESS_LEVEL, "No active project set")
            return []
        
        if tree == "assets":
            group_type = "groups"
        elif tree == "shots":
            group_type = "sequences"
        else:
            raise WoodyError(f"'{tree}' is not a vaild search term, use shots/assets", label="Warning", level="warning")
        
        self.db.use(self.guard._current_project, tree)
        results = self.db.run(self.db.get_all())
        if not results:
            woody_logger.log(SUCCESS_LEVEL, f"No {group_type} found in {tree}")
            return []
        
        field = 'sequence' if tree == 'shots' else 'group'
        groups = {item[field] for item in results if field in item}
        
        if not groups:
            woody_logger.log(SUCCESS_LEVEL, f"No {group_type} found in {tree}")
            return []
        
        sorted_groups = sorted(groups)
        
        group_list = '\n'.join(f"  - {group}" for group in sorted_groups)
        msg = f"Available {group_type}:\n{group_list}"
        woody_logger.log(SUCCESS_LEVEL, msg)
        
        return sorted_groups

    def list_names(self, tree, group):
        if not self.db or not self.guard._current_project:
            woody_logger.log(SUCCESS_LEVEL, "No active project set")
            return []
        
        self.db.use(self.guard._current_project, tree)
        results = self.db.run(self.db.get_all())
        if not results:
            woody_logger.log(SUCCESS_LEVEL, f"No items found in {tree}")
            return []
        
        field = 'sequence' if tree == 'shots' else 'group'
        names = {item['name'] for item in results if item.get(field) == group and 'name' in item}
        
        if not names:
            woody_logger.log(SUCCESS_LEVEL, f"No items found in {group}")
            return []
        
        sorted_names = sorted(names)
            
        name_list = '\n'.join(f"  - {name}" for name in sorted_names) 
        item_type = "shots" if tree == "shots" else "assets"
        msg = f"Available {item_type} in {group}:\n{name_list}"
        woody_logger.log(SUCCESS_LEVEL, msg)
        
        return sorted_names