import json
from pathlib import Path

def create_default_proj_config(path: Path):
    default_config = {
        "render_settings": {
            "resolution_x": 1920,
            "resolution_y": 1080,
            "fps": 24,
            "file_format": "OPEN_EXR_MULTILAYER",
            "exr_codec": "DWAA",
            "engine": "CYCLES",
            "use_motion_blur": True,
            "motion_blur_shutter": 0.5,
            "film_transparent": True,
            "use_simplify": True,
            "simplify_subdivision": 2,
            "simplify_subdivision_render": 5,
            "cycles_samples": 512,
            "use_persistent_data": True,
        }
    }

    config_path = path / "projConfig.json"
    with config_path.open("w") as f:
        json.dump(default_config, f, indent=2)