from woody.pywoody.core.console import WoodyError
from woody.pywoody.handlers.processor import Processor

import argparse

def create(self, args):
    """Create new projects or assets using flags"""
    parser = argparse.ArgumentParser(prog='create', exit_on_error=False)
    parser.add_argument('-a', '--asset', nargs=2, metavar=('GROUP', 'NAME'))
    parser.add_argument('-pr', '--project', type=str, metavar='NAME')
    parser.add_argument('-p', '--publish', nargs=2, metavar=('NAME', 'TYPE'))
    parser.add_argument('-s', '--shot', nargs=4, metavar=('GROUP', 'NAME', 'START', 'END'))
    parser.add_argument('-sc', '--scene', nargs=2, metavar=('NAME', 'DCC'))
    
    parsed = self._parse_args(parser, args)
    
    if parsed is None:
        return 
    
    if parsed.project:
        Processor().create_project(parsed.project)
    
    elif parsed.asset:
        group, asset_name = parsed.asset
        Processor().create_asset(group, asset_name)
            
    elif parsed.shot:
        if len(parsed.shot) < 2:
            raise WoodyError("Shot requires at least SEQUENCE and NAME")
        group, shot_name = parsed.shot[0], parsed.shot[1]
        start_frame = int(parsed.shot[2]) if len(parsed.shot) > 2 else None
        end_frame = int(parsed.shot[3]) if len(parsed.shot) > 3 else None
        Processor().create_shot(group, shot_name, start_frame, end_frame)
        
    elif parsed.scene:
        scene_name, dcc = parsed.scene
        Processor().create_scene(scene_name, dcc)
    
    elif parsed.publish:
        publish_name, publish_type = parsed.publish
        Processor().create_publish(publish_name, publish_type)
    
    else:
        raise WoodyError("No valid flags provided. Use -pr/--project, -a/--asset, or -p/--publish")
    