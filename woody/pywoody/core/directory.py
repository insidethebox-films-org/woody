import pathlib
import shutil
from typing import Dict, Any
from ..objects.guard import Guard
from ..core.console import woody_logger, SUCCESS_LEVEL 

class Directory:
    """
    A utility class to manage directory creation, deletion, and validation.
    """
    guard = Guard()

    def __init__(self):
        if self.guard._preferences:
            self.base_path = pathlib.Path(self.guard._preferences.get("projects_directory"))
        else:
            self.base_path = None

    def create(self, structure: Dict[str, Any]):
        """
        Public method to start the recursive creation process.
        Returns the final (deepest) path created.
        """
        if not self.base_path:
            msg = "Base path not set - preferences not loaded"
            woody_logger.error(msg)
            raise ValueError(msg)
            
        final_path = self._create_recursive(self.base_path, structure)
        return final_path

    def _create_recursive(self, current_path: pathlib.Path, tree: Dict[str, Any]):
        """
        Internal recursive method to navigate the dictionary.
        Returns the deepest path created.
        """
        deepest_path = current_path
        
        for folder_name, contents in tree.items():
            new_folder = current_path / folder_name
            new_folder.mkdir(parents=True, exist_ok=True)
            deepest_path = new_folder

            if isinstance(contents, dict):
                deepest_path = self._create_recursive(new_folder, contents)
            elif isinstance(contents, list):
                for sub_item in contents:
                    created_path = new_folder / sub_item
                    created_path.mkdir(parents=True, exist_ok=True)
                    deepest_path = created_path
        
        return deepest_path