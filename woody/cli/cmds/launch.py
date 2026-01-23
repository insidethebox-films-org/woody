from woody.pywoody.core.console import WoodyError
from woody.pywoody.handlers.processor import Processor

import argparse

def launch(self, args):
    """Launch DCC applications"""
    parser = argparse.ArgumentParser(prog='launch', exit_on_error=False)
    parser.add_argument('-b', '--blender', action='store_true')
    
    parsed = self._parse_args(parser, args)
    
    if parsed is None:
        return 
    
    if parsed.blender:
        Processor().launch_blender()
    
    else:
        raise WoodyError("No valid flags provided. Use -b/--blender")