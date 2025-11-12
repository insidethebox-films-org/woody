import subprocess
import platform
from pathlib import Path

def get_python_path(blender_path):
    
    """
    Returns the path to Blender's bundled Python executable and its site-packages directory.
    Works on macOS, Windows, and Linux, automatically detecting the Blender version folder.
    """
    system = platform.system()
    blender_path = Path(blender_path)

    # --- macOS ---
    if system == "Darwin":
        if ".app" in blender_path.parts:
            app_index = blender_path.parts.index(next(p for p in blender_path.parts if p.endswith(".app")))
            blender_path = Path(*blender_path.parts[:app_index + 1])
        else:
            while blender_path and blender_path.name != "Blender.app":
                blender_path = blender_path.parent

        resources = blender_path / "Contents" / "Resources"
        version_dirs = [d for d in resources.iterdir() if (d / "python").exists()]

    # --- Windows ---
    elif system == "Windows":
        resources = blender_path
        version_dirs = [d for d in resources.iterdir() if (d / "python" / "bin" / "python.exe").exists()]

    # --- Linux ---
    else:
        resources = blender_path
        version_dirs = [d for d in resources.iterdir() if (d / "python" / "bin").exists()]

    if not version_dirs:
        print(f"No Blender version folder with Python found in {resources}")
        return None, None

    version_dirs.sort(reverse=True)
    version_dir = version_dirs[0]
    python_root = version_dir / "python"
    python_bin = python_root / "bin"

    if system == "Windows":
        python_exe = python_bin / "python.exe"
    else:
        python_exe = next(python_bin.glob("python3.*"), python_bin / "python3")

    try:
        result = subprocess.run(
            [str(python_exe), "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            capture_output=True, text=True, check=True
        )
        py_version = result.stdout.strip()
    except Exception:
        py_version = "3.11"

    if system == "Windows":
        site_packages = python_root / "Lib" / "site-packages"
    else:
        site_packages = python_root / "lib" / f"python{py_version}" / "site-packages"

    return python_exe, site_packages


def install_blender_libraries(blender_executable_path: str) -> bool:
    
    blender_path = Path(blender_executable_path)
    python_exe, site_packages = get_python_path(blender_path)
    
    if not python_exe or not python_exe.exists():
        print(f"Error: Blender Python not found at {python_exe}")
        return False
    
    print(f"Installing to: {python_exe}")
    print(f"Target: {site_packages}")
    
    libraries = ["pymongo"]
    
    for library in libraries:
        print(f"\nInstalling {library}...")
        
        result = subprocess.run([
            str(python_exe), "-m", "pip", "install",
            "--target", str(site_packages),
            "--force-reinstall",
            library
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        
        verify = subprocess.run([
            str(python_exe), "-c",
            f"import sys; sys.path.insert(0, r'{site_packages}'); "
            f"import {library}; print('SUCCESS')"
        ], capture_output=True, text=True)
        
        if verify.returncode == 0:
            print(f"✓ {library} installed successfully")
        else:
            print(f"✗ Verification failed: {verify.stderr}")
            return False
        
    return True