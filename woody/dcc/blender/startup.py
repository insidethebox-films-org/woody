"""
Woody Blender Startup Script
This script is executed when Blender launches with Woody integration
Registers the Woody addon and initializes the Woody environment.
"""

import sys
from pathlib import Path
from woody.pywoody import Woody

# Get the addon directory
addon_dir = Path(__file__).parent

# Add to sys.path if not already there
addon_dir_str = str(addon_dir)
if addon_dir_str not in sys.path:
    sys.path.insert(0, addon_dir_str)

# Import and register the Woody addon
try:
    import woody_addon
    woody_addon.register()
    Woody().run()
    print("Woody addon registered successfully!")
except Exception as e:
    print(f"Failed to register Woody addon: {e}")
