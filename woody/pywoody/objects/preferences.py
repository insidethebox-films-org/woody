import os
from pathlib import Path

from woody import PACKAGE_ROOT
from ..core.io import IO
from ..core.database import get_db
from ..core.console import woody_logger, SUCCESS_LEVEL
from .guard import Guard


class Preferences():
    guard = Guard()
    
    def __init__(self):
        self.prefs_path = PACKAGE_ROOT.parent / "prefs" / "prefs.json"
        self.io = IO(self.prefs_path)

    @property
    def db(self):
        return get_db()
    
    def check(self):
        if os.path.exists(self.prefs_path):
            prefs = self.io.load()
            self.guard.set_preferences(prefs)
            return True
        return False
        
    def create(self, user: str, projects_path: str, mongodb_address: str):
        self.prefs_path.parent.mkdir(parents=True, exist_ok=True)
        
        prefs = {
            "user": user,
            "projects_directory": projects_path, 
            "mongodb_address": mongodb_address
        }
        
        self.guard.set_preferences(prefs)
        
        self.io.save(prefs)
        
    def update(self, **kwargs):
        self.io.update(kwargs)
        
        updated_prefs = self.io.load()
        self.guard.set_preferences(updated_prefs)
        
        woody_logger.log(SUCCESS_LEVEL, "Preferences updated")
    
    def load(self):
        prefs = self.io.load()
        return prefs
    
    def switch_projects(self, project_name: str):
        projects = self.db.run(self.db.list_projects())
        
        if project_name not in projects:
            msg = f"{project_name} is not an existing project"
            woody_logger.warning(msg)
            return msg
        
        project = {"current_project": project_name}
        self.io.update(project)
        self.guard.set_current_project(project_name)
        self.guard.set_context(None)
        
        msg = f"Switched to project: {project_name}"
        woody_logger.log(SUCCESS_LEVEL, msg)
        
        return msg
        