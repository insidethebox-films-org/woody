from pathlib import Path
import json

settings_path  = Path("prefs") / "prefs.json"
settings_path.parent.mkdir(parents=True, exist_ok=True)

def save_settings_json(mongoDBAddress=None, blenderExecutable=None, projectName=None):
        
    # Load existing settings first
    existing_settings = load_settings_json() or {}
    
    # Only update the values that are provided (not None)
    if mongoDBAddress is not None:
        existing_settings["mongoDBAddress"] = mongoDBAddress
    if blenderExecutable is not None:
        existing_settings["blenderExecutable"] = blenderExecutable
    if projectName is not None:
        existing_settings["projectName"] = projectName

    with settings_path.open("w", encoding="utf-8") as f:
        json.dump(existing_settings, f, indent=4, ensure_ascii=False)
        
def load_settings_json():

    if not settings_path.exists():
        print(f"No preferences file found at {settings_path}")
        return None
    
    with settings_path.open("r", encoding="utf-8") as f:
        settings = json.load(f)
        
    return settings
    