from .directory_instance import DirectoryInstance

def create_element_fd(groupTypeCombo, groupName, elementName):
      
    group_type = "assets" if groupTypeCombo == "Assets Group" else "shots"

    dirInstance = DirectoryInstance()
    base_path = dirInstance.root_path / group_type / groupName
    
    folders = {
       elementName: [],
    }
    dirInstance.create_folders_subfolders(base_path, folders)
    