import json
import os
from typing import Any, Dict, Optional, Union

class IO:
    """
    A utility class for reading from and writing to JSON files.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath

    def save(self, data: Union[Dict, list], indent: int = 4) -> bool:
        """
        Serializes data to the JSON file.
        
        :param data: The dictionary or list to save.
        :param indent: Spaces for nesting (default 4).
        :return: True if successful, False otherwise.
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            return True
        except (IOError, TypeError) as e:
            print(f"Error saving JSON to {self.filepath}: {e}")
            return False

    def load(self) -> Optional[Union[Dict, list]]:
        """
        Reads and parses the JSON file.
        
        :return: The parsed data or None if the file doesn't exist or is invalid.
        """
        if not os.path.exists(self.filepath):
            print(f"File not found: {self.filepath}")
            return None

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading JSON from {self.filepath}: {e}")
            return None

    def update(self, new_data: Dict) -> bool:
        """
        Loads existing data, updates it with new_data, and saves it back.
        Only works if the top-level structure is a dictionary.
        """
        current_data = self.load()
        
        if current_data is None:
            current_data = {}
        
        if isinstance(current_data, dict):
            current_data.update(new_data)
            return self.save(current_data)
        else:
            print("Update failed: Existing JSON structure is not a dictionary.")
            return False