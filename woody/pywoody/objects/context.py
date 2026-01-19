from ..core.database import get_db
from .guard import Guard
from .woody_id import WoodyID
from ..core.console import WoodyError

class Context():
    guard = Guard()
    
    def __init__(self, tree: str, group: str, asset: str, product_type: str = None, product_name: str = None):
        self.db = get_db()
        
        self.tree = tree
        self.group = group
        self.asset = asset
        
        self.product_type = product_type
        self.product_name = product_name
        
        self.woody_id = WoodyID().create(
            self.guard._current_project, 
            [self.tree, self.group, self.asset],
            self.product_type,
            self.product_name
        )
        
    def set_context(self):
        if self.product_type:
            self.db.use(self.guard._current_project, self.product_type)
        else:
            self.db.use(self.guard._current_project, self.tree)
        
        if not self.db.run(self.db.ensure_unique("woody_id")):
            raise WoodyError(f"Context with ID '{self.woody_id}' does not exist")
        
        self.guard.set_context([self.tree, self.group, self.asset, self.product_type, self.product_name])
        
        return f"Switched context to [{self.tree}/{self.group}/{self.asset}/{self.product_type}/{self.product_name}]"