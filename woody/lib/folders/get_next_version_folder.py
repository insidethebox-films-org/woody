import re

def get_next_version_folder(base_path):
    version_pattern = re.compile(r"v(\d+)")
    versions = []

    for item in base_path.iterdir():
        if item.is_dir():
            match = version_pattern.fullmatch(item.name)
            if match:
                versions.append((int(match.group(1)), item))

    if not versions:
        return base_path / "v1"

    # Sort by version number descending
    versions.sort(reverse=True)
    latest_version_num, latest_version_path = versions[0]

    # Check if the latest version folder has any files inside
    if any(latest_version_path.iterdir()):
        # Folder is not empty → increment version
        return base_path / f"v{latest_version_num + 1}"
    else:
        # Folder is empty → reuse it
        return latest_version_path