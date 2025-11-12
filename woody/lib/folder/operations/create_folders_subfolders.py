import os

def create_folders_subfolders(base_path, folders):
        
        if base_path is None:
            print("Error: Could not mount the drive. Cannot create directories.")
            return
        
        # Use the mounted local path for directory creation
        for main_folder, subfolders in folders.items():
            main_path = os.path.join(base_path, main_folder)
            try:
                print(f"Creating directory: {main_path}")
                os.makedirs(main_path, exist_ok=True)
                print(f"SUCCESS: Created {main_path}")
            except OSError as e:
                print(f"Could not create directory {main_path}: {e}")
                continue

            if isinstance(subfolders, dict):
                # For nested dictionaries, recursively create subdirectories
                for subfolder_name, nested_content in subfolders.items():
                    subfolder_path = os.path.join(main_path, subfolder_name)
                    try:
                        print(f"Creating directory: {subfolder_path}")
                        os.makedirs(subfolder_path, exist_ok=True)
                        print(f"SUCCESS: Created {subfolder_path}")
                    except OSError as e:
                        print(f"Could not create directory {subfolder_path}: {e}")
                        
            elif isinstance(subfolders, list): 
                for subfolder in subfolders:
                    subfolder_path = os.path.join(main_path, subfolder)
                    try:
                        print(f"Creating directory: {subfolder_path}")
                        os.makedirs(subfolder_path, exist_ok=True)
                        print(f"SUCCESS: Created {subfolder_path}")
                    except OSError as e:
                        print(f"Could not create directory {subfolder_path}: {e}")