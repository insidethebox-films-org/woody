from woody.pywoody.core.console import WoodyError
from woody.pywoody.handlers.processor import Processor

def set_context(self, args):
    """Change current working context (tree/group/asset)"""
    if len(args) < 3:
        raise WoodyError("Context requires 3 arguments: <tree> <group> <asset>")
    
    product_type = args[3] if len(args) > 3 else None
    product_name = args[4] if len(args) > 4 else None
    
    Processor().set_context(tree=args[0], group=args[1], asset=args[2], product_type=product_type, product_name=product_name)

def switch_projects(self, args):
    """Switch to a different active project"""
    if not args:
        raise WoodyError("Project name required")
    
    Processor().switch_projects(project_name=args[0])