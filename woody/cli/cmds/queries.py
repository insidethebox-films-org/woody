from woody.pywoody.core.console import WoodyError
from woody.pywoody.handlers.processor import Processor

import argparse

def list(self, args):
    """List created entities with flags"""
    parser = argparse.ArgumentParser(prog='list', exit_on_error=False)
    parser.add_argument('-p', '--project', action='store_true')
    parser.add_argument('-g', '--group', nargs='?', const=True, metavar='TREE')
    parser.add_argument('-n', '--name', nargs='*', metavar='TREE_OR_GROUP')  # Accept 0, 1, or 2 args
    
    parsed = self._parse_args(parser, args)
    
    if parsed is None:
        return 
    
    if parsed.project:
        Processor().list_projects()
    
    elif parsed.group is not None:
        processor = Processor()
        
        if parsed.group is True: 
            current_tree = processor.guard._context.get("tree")
            if not current_tree:
                raise WoodyError("No tree set in context. Set context first with 'context <tree>'")
            tree = current_tree
        else:  
            tree = parsed.group
            
        processor.list_groups(tree)
        
    elif parsed.name is not None:  
        processor = Processor()
        
        if len(parsed.name) == 0: 
            current_tree = processor.guard._context.get("tree")
            current_group = processor.guard._context.get("group")
            
            if not current_tree or not current_group:
                raise WoodyError("No tree/group set in context. Set context first with 'context <tree>' then 'context <group>'")
                
            tree, group = current_tree, current_group
            
        elif len(parsed.name) == 1:  
            current_tree = processor.guard._context.get("tree")
            if not current_tree:
                raise WoodyError("No tree set in context. Set context first with 'context <tree>'")
                
            tree, group = current_tree, parsed.name[0]
            
        elif len(parsed.name) == 2: 
            tree, group = parsed.name[0], parsed.name[1]
            
        else:
            raise WoodyError("Too many arguments for --name. Provide 0, 1, or 2 arguments.")
            
        processor.list_names(tree, group)
        
    else:
        raise WoodyError("No valid flags provided. Use -p/--project, -g/--group, or -n/--name")