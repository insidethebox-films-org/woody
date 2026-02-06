from woody.pywoody.core.console import WoodyError, woody_logger, SUCCESS_LEVEL
from woody.pywoody.handlers.processor import Processor

def set_context(self, args):
    """Change current working context incrementally or fully"""
    processor = Processor()
    
    if "--clear" in args:
        processor.clear_context()
        return
    
    if "--get" in args:
        print(processor.get_context())
        return
    
    if not args:
        print(processor.get_context())
        return
    
    processor.set_context(args)

def switch_projects(self, args):
    """Switch to a different active project"""
    if not args:
        raise WoodyError("Project name required")
    
    result = Processor().switch_projects(project_name=args[0])
    print(result)