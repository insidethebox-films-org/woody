from .directory_instance import DirectoryInstance

def create_project_fd(project_name):

    dir_instance = DirectoryInstance(project_name)
    base_path = dir_instance.root_path
    
    folders = {
        "assets": [],
        "shots": [],
    }
    dir_instance.create_folders_subfolders(base_path, folders)
