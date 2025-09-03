def create_folders_subfolders(folders, base_path):
    for main_folder, subfolders in folders.items():
        main_path = base_path / main_folder
        main_path.mkdir(parents=True, exist_ok=True)

        if isinstance(subfolders, dict):
            create_folders_subfolders(subfolders, main_path)
        elif isinstance(subfolders, list): 
            for subfolder in subfolders:
                (main_path / subfolder).mkdir(parents=True, exist_ok=True)