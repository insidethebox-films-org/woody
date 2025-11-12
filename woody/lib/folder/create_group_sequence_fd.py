from .directory_instance import DirectoryInstance

def create_group_sequence_fd(type, folder_name):
    
    group_type = "assets" if type == "Assets Group" else "shots"
    
    dirInstance = DirectoryInstance()
    base_path = dirInstance.root_path / group_type
    
    folders = {
       folder_name: [],
    }
    dirInstance.create_folders_subfolders(base_path, folders)
    
    