import os

from ...tool.woody_instance import WoodyInstance
from ...database.db_instance import DB_instance
from ...lib.folder.directory_instance import DirectoryInstance
from .operations import *

class BlenderInstance:
    def __init__(self):
        self.woody = WoodyInstance()
        self.db = DB_instance()
        self.executable = set_executable_path(self.woody.blenderExecutable)

        self.addon_dir = get_addon_dir(self.woody.blenderExecutable)
        self.addon_zip = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../woody_blender_addon.zip")) #TODO hardcoded path

    
    def create_file(self, group_type: str, group_name: str, element_name: str, blend_name: str) -> bool:
        """Creates a new blend file"""
        if not self.executable or not os.path.exists(self.executable):
            print(f"Invalid Blender executable path: {self.executable}")
            return False
        
        blend_path = DirectoryInstance().construct_path([group_type, group_name, element_name, blend_name])
        
        return create_blend_file(self.executable, blend_path)

    def open_file(self, group_type: str, group_name: str, element_name: str, blend_name: str) -> bool:
        """Opens existing blend file with addon update check"""
        if not self.executable or not os.path.exists(self.executable):
            print(f"Invalid Blender executable path: {self.executable}")
            return False
        
        blend_path = DirectoryInstance().construct_path([group_type, group_name, element_name, blend_name])
        print(blend_path)
        
        return open_blend_file(self.executable, blend_path, self.addon_zip)
    
    def dev_update(self) -> bool:
        """Updates the addon zip file for development"""
        return update_zip_dev(self.addon_zip)
    
    # def get_blend_path(self, group_type: str, group_name: str, element_name: str, blend_name: str) -> str:
    #     """Gets the blend file path for given parameters"""
    #     return get_blend_path(
    #         str(self.db.projectDirectory),
    #         str(self.woody.projectName),
    #         group_type,
    #         group_name,
    #         element_name,
    #         blend_name,
    #     )