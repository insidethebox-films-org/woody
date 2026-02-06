class Guard:
    _preferences = None
    _current_project = None
    _context = {"tree": None, "group": None, "asset": None, "product_type": None, "product_name": None}
    _current_path = None
    
    @classmethod
    def set_preferences(cls, preferences: dict):
        cls._preferences = preferences
        
    @classmethod
    def set_current_project(cls, project_name: str):
        cls._current_project = project_name
    
    @classmethod    
    def set_context(cls, **kwargs):
        """Set context values directly"""
        for key, value in kwargs.items():
            if key in cls._context:
                cls._context[key] = value
    
    @classmethod
    def clear_context(cls):
        """Clear all context"""
        cls._context = {"tree": None, "group": None, "asset": None, "product_type": None, "product_name": None}