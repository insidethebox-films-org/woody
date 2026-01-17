from woody.pywoody.core.console import WoodyError
from woody.pywoody.handlers.processor import Processor

import argparse
import json

def update(self, args):
    """Update metadata: -p '{"key":"value"}' | -a '{"key":"value"}'"""
    parser = argparse.ArgumentParser(prog='update', exit_on_error=False)
    parser.add_argument('-p', '--project', type=str, metavar='JSON')
    parser.add_argument('-a', '--asset', type=str, metavar='JSON')
    
    parsed = self._parse_args(parser, args)
    
    if parsed is None:
        return 
    
    if parsed.project:
        try:
            data = json.loads(parsed.project)
        except json.JSONDecodeError:
            raise WoodyError("Invalid JSON format. Use: -p '{\"key\":\"value\"}'")
        
        Processor().update_project(data)
        
    elif parsed.asset:
        try:
            data = json.loads(parsed.asset)
        except json.JSONDecodeError:
            raise WoodyError("Invalid JSON format. Use: -a '{\"key\":\"value\"}'")

        Processor().update_asset(data)

    
    else:
        raise WoodyError("No valid flags provided. Use -p/--project or -a/--asset")
    

    