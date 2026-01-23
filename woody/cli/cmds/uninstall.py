from woody.pywoody.core.console import WoodyError
from woody.pywoody.handlers.processor import Processor

import argparse

def uninstall(self, args):
    """Uninstall Woody from DCC's based on flags: -blender 'exe_path'"""
    parser = argparse.ArgumentParser(prog='install', exit_on_error=False)
    parser.add_argument('-b', '--blender', action='store_true')
    
    parsed = self._parse_args(parser, args)
    
    if parsed is None:
        return 
    
    if parsed.blender:
        Processor().uninstall_blender()
    
    else:
        raise WoodyError("No valid flags provided. Use -b/--blender")