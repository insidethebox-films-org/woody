from ..utils import load_settings_json

class WoodyInstance():
    _instance = None
    _browser_selection_data = None 
    _asset_details = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WoodyInstance, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        settings = load_settings_json() or {}
        
        self.projectName = settings.get("projectName")
        self.mongoDBAddress = settings.get("mongoDBAddress")
        self.blenderExecutable = settings.get("blenderExecutable")
    
    @classmethod
    def browser_selection(cls, selection_data=None):
        if selection_data is not None:
            cls._browser_selection_data = selection_data
        return cls._browser_selection_data
    
    @classmethod
    def asset_details(cls, doc=None):
        if doc is not None:
            cls._asset_details = doc
        return cls._asset_details
    