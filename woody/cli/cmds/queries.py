from woody.pywoody.core.console import WoodyError
from woody.pywoody.handlers.processor import Processor

import argparse

def list(self, args):
    """List created entities with flags"""
    parser = argparse.ArgumentParser(prog='list', exit_on_error=False)
    parser.add_argument('-p', '--project', action='store_true')
    parser.add_argument('-g', '--group', nargs=1, metavar=('GROUP_TYPE'))
    parser.add_argument('-n', '--name', nargs=2, metavar=('GROUP_TYPE', 'NAME'))
    # parser.add_argument('-sc', '--scene', nargs=2, metavar=('NAME', 'DCC'))
    
    parsed = self._parse_args(parser, args)
    
    if parsed is None:
        return 
    
    if parsed.project:
        Processor().list_projects()
    
    elif parsed.group:
        group_type = parsed.group[0]
        Processor().list_groups(group_type)
        
    elif parsed.name:
        group_type, name = parsed.name
        Processor().list_names(group_type, name)
        
    # elif parsed.scene:
    #     scene_name, dcc = parsed.scene
    #     Processor().create_scene(scene_name, dcc)
    
    else:
        raise WoodyError("No valid flags provided. Use -p/--project or -a/--asset")
    