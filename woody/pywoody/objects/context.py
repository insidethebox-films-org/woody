from ..core.database import get_db
from ..core.queries import Queries
from .guard import Guard
from ..core.console import WoodyError, quiet, woody_logger

@quiet
def _list_groups(tree):
    return Queries().list_groups(tree)

@quiet
def _list_names(tree, group):
    return Queries().list_names(tree, group)
    
class Context():
    guard = Guard()
    
    def __init__(self, tree: str = None, group: str = None, asset: str = None, product_type: str = None, product_name: str = None):
        self.db = get_db()
        
        self.context = [tree, group, asset, product_type, product_name]
    
    def set(self, value=None):
        
        if value == None:
            value = self.context
        else: 
            values = []
            
        if isinstance(value, list):
            values = value
        elif value:
            values = [value]
        else:
            values = [v for v in self.context if v is not None]
      
        if values and values[0] in ["assets", "shots"]:
            self.guard.clear_context()

        levels = ["tree", "group", "asset", "product_type", "product_name"]
        
        for i, val in enumerate(values):
            current_depth = len([v for v in self.guard._context.values() if v is not None])
            
            if current_depth >= len(levels):
                raise WoodyError("Context is already complete")
            
            level = levels[current_depth]
            
            if level == "tree":
                trees = ["assets", "shots"]
                if val not in trees:
                    raise WoodyError(f"Tree '{val}' does not exist in project '{self.guard._current_project}'")
                    
            elif level == "group":
                current_tree = self.guard._context.get("tree")
                groups = _list_groups(current_tree)
                group_list = '\n'.join(f"  - {group}" for group in groups)
                
                if val not in groups:
                    raise WoodyError(f"Group '{val}' does not exist in tree '{current_tree}'\nTry these:\n{group_list}")
                    
            elif level == "asset":
                current_tree = self.guard._context.get("tree")
                current_group = self.guard._context.get("group")
                
                assets = _list_names(current_tree, current_group)
                name_list = '\n'.join(f"  - {name}" for name in assets) 
                if val not in assets:
                    raise WoodyError(f"Asset '{val}' does not exist in {current_tree}/{current_group}\nTry these:\n{name_list}")
            
            self.guard._context[level] = val
        
        final_depth = len([v for v in self.guard._context.values() if v is not None])
        for i in range(final_depth, len(levels)):
            self.guard._context[levels[i]] = None
    
    def get(self):
        context = self.guard._context
        formated_context = {}
        for key, value in context.items():
            if value is not None:
                formated_context[key] = value
        woody_logger.info("Current Context:")
        return formated_context