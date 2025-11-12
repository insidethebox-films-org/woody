from ...database.db_instance import DB_instance
from .operations import mount_drive
from .operations import create_folders_subfolders

import platform
from pathlib import Path

class DirectoryInstance():

    def __init__(self, project_name=None):
        
        if project_name:
            settings = DB_instance(project_name).get_docs(collection="settings")[0]
        else:
            settings = DB_instance().get_docs(collection="settings")[0]
        
        self.project_name = settings.get("project_name")
        self.host_address = settings.get("host_address")
        self.location = settings.get("location")
        
        self.mount_local_drive(self.host_address, self.location)
        
        self.root_path = self.get_root_path(self.host_address, self.location,  self.project_name)

    def get_root_path(self, host_address, location, project_name):

        current_os = platform.system()

        if current_os == 'Darwin':
            return Path(f"/Volumes/{location}/{project_name}/".replace('\\', '/'))
        elif platform.system() == "Windows":
            return Path(f"\\\{host_address}\\{location}\\{project_name}\\")
        else:
            print("System not recognized")
            return None
        
    def construct_path(self, subfolders=[]):
    
        path = self.root_path
        
        for i in subfolders:
            path = path / i
        
        return path
    
    def mount_local_drive(self, host_address, location):
        return mount_drive(host_address, location) 

    def create_folders_subfolders(self, base_path, folders):
        return create_folders_subfolders(base_path, folders)

