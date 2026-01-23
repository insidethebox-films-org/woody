import subprocess
from pathlib import Path
from ..core.console import woody_logger, WoodyError, SUCCESS_LEVEL

class DCC:
    def __init__(self, dcc):
        self.dcc = dcc
        self.project_root = self._find_project_root()
    
    def _find_project_root(self):
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "pyproject.toml").exists():
                return parent
        raise WoodyError("Could not find pyproject.toml", "error", "Error")
    
    def install(self, exe, python_path, force_update=False):
        app_root = Path(exe).parent
        
        python_exe = app_root / python_path / "python.exe"
        
        if not python_exe.exists():
            raise WoodyError(f"Python not found at {python_exe}", "error", "Error")
        
        woody_logger.info(f"Installing woody to {self.dcc}")
        
        subprocess.run([str(python_exe), "-m", "pip", "uninstall", "woody", "-y"], check=False)
        
        cmd = [str(python_exe), "-m", "pip", "install", "-e", str(self.project_root)]
        if force_update:
            cmd.append("--upgrade")
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            raise WoodyError(f"Failed to install woody to {self.dcc}", "error", "Error")
        
        test_cmd = [str(python_exe), "-c", "import woody; print('woody installed successfully')"]
        subprocess.run(test_cmd, check=False)
        
        woody_logger.log(SUCCESS_LEVEL, f"{self.dcc} install complete!")
        return True
    
    def uninstall(self, exe, python_path):
        app_root = Path(exe).parent
        python_exe = app_root / python_path / "python.exe"
        
        if not python_exe.exists():
            raise WoodyError(f"Python not found at {python_exe}", "error", "Error")
        
        woody_logger.info(f"Uninstalling woody from {self.dcc}")
        
        result = subprocess.run([str(python_exe), "-m", "pip", "uninstall", "woody", "-y"], 
                              capture_output=True, text=True)
        
        if "Cannot uninstall requirement woody" in result.stderr:
            woody_logger.info(f"woody was not installed in {self.dcc}")
        elif "Successfully uninstalled woody" in result.stdout:
            woody_logger.info(f"woody successfully removed from {self.dcc}")
        
        woody_logger.log(SUCCESS_LEVEL, f"Uninstall completed for {self.dcc}!")
        return True