from woody.pywoody.objects.dcc import DCC
from woody.pywoody.objects.preferences import Preferences
from woody.pywoody.objects.guard import Guard
from woody.pywoody.core.console import WoodyError

from pathlib import Path
import subprocess

class Blender():
    guard = Guard()
    
    def __init__(self):
        self.prefs = Preferences()
        self.dcc = DCC("Blender")
        self.exe = self.guard._preferences.get("blender_exe") or None

    def _find_python_path(self, exe_path):
        exe_file = Path(exe_path)
        app_root = exe_file.parent
        
        if not app_root.exists():
            raise WoodyError(f"Blender directory not found: {app_root}", "error")
        
        for item in app_root.iterdir():
            if item.is_dir():
                python_bin = item / "python" / "bin"
                python_exe = python_bin / "python.exe"
                
                if python_bin.exists() and python_exe.exists():
                    return python_bin.relative_to(app_root)
        
        raise WoodyError("Could not find Python installation in Blender directory", "error")
    
    def install(self, exe, force_update=False):
        self.dcc.install(exe, self._find_python_path(exe), force_update)
        self.prefs.update(blender_exe=exe)
        self.exe = self.guard._preferences.get("blender_exe")
        
    def uninstall(self):
        if not self.exe:
            raise WoodyError("Blender executable not set. Cannot uninstall.", "error")
        
        return self.dcc.uninstall(self.exe, self._find_python_path(self.exe))
        
    def launch(self):
        if self.exe:
            startup_script = Path(__file__).parent / "startup.py"
            subprocess.run([str(self.exe), "--python", str(startup_script)])
        else:
            raise WoodyError("Blender executable not set. Run install first.", "error")