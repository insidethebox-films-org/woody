class Guard():
    _preferences = None
    _current_project = None
    _context = None
    _current_path = None
    
    def __init__(cls):
        cls.set_current_path()
    
    @classmethod
    def set_preferences(cls, preferences: dict):
        cls._preferences = preferences
        
    @classmethod
    def set_current_project(cls, project_name: str):
        cls._current_project = project_name
    
    @classmethod    
    def set_context(cls, context: list):
        cls._context = context
        
    def set_current_path(cls):
        ...