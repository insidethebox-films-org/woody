import json
from pathlib import Path

def create_shot_config_file(config_path: Path, config_data: dict):
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4)