import bpy
import json

def apply_render_config(config_path: str):
    
    with open(config_path, 'r') as f:
        config = json.load(f)

    render = bpy.context.scene.render
    image_settings = render.image_settings
    cycles = bpy.context.scene.cycles
    settings = config.get("render_settings", {})

    # Resolution & Frame Rate
    render.resolution_x = settings.get("resolution_x", render.resolution_x)
    render.resolution_y = settings.get("resolution_y", render.resolution_y)
    render.fps = settings.get("fps", render.fps)

    # File Output
    image_settings.file_format = settings.get("file_format", image_settings.file_format)
    image_settings.exr_codec = settings.get("exr_codec", image_settings.exr_codec)

    # Render Engine
    render.engine = settings.get("engine", render.engine)

    # Motion Blur
    render.use_motion_blur = settings.get("use_motion_blur", render.use_motion_blur)
    render.motion_blur_shutter = settings.get("motion_blur_shutter", render.motion_blur_shutter)

    # Film Settings
    render.film_transparent = settings.get("film_transparent", render.film_transparent)

    # Simplify
    render.use_simplify = settings.get("use_simplify", render.use_simplify)
    render.simplify_subdivision = settings.get("simplify_subdivision", render.simplify_subdivision)
    render.simplify_subdivision_render = settings.get("simplify_subdivision_render", render.simplify_subdivision_render)

    # Cycles samples
    cycles.samples = settings.get("cycles_samples", cycles.samples)

    # Persistent Data
    render.use_persistent_data = settings.get("use_persistent_data", render.use_persistent_data)
    

    print(f"[apply_render_config]✅ Render settings applied from {config_path}")