import os
import hashlib

def get_zip_hash(zip_path: str) -> str:
        """Get hash of addon zip file
        
        Returns:
            str: MD5 hash of the addon zip file, or empty string if not found
        """
        if not os.path.exists(zip_path):
            return ""
        with open(zip_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()