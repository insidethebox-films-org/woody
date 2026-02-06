from enum import Enum
import os

class WoodyIcon(Enum):
    ICON = "woodyIcon.ico"
    HEADER = "woodyHeader.png"
    CREATE_ELEMENT = "create_element.png"
    CREATE_GROUP = "create_group.png"

    @property
    def path(self):
        base_dir = os.path.join(os.path.dirname(__file__), "..", "icons", "images")
        return os.path.abspath(os.path.join(base_dir, self.value))