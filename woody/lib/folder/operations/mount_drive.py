import platform
import os
import subprocess

def mount_drive(host_address, location):
    
    current_os = platform.system()

    if current_os == 'Darwin':
        host_address = host_address.replace('\\', '/')
        location = location.replace('\\', '/')
        
        # Mount point
        mount = f"/Volumes/{location}"
        
        if not os.path.ismount(mount):
            smb_url = f"smb://{host_address}/{location}"
            print(f"Mounting {smb_url} to {mount}...")

            result = subprocess.run(
                ['osascript', '-e', 
                    f'mount volume "{smb_url}"'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                print(f"Warning: Could not mount {smb_url}: {result.stderr}")
                return False
            
            # Verify the mount was successful
            if os.path.ismount(mount):
                print(f"Successfully mounted {smb_url}")
                return True
            else:
                print(f"Mount verification failed: {mount}")
                return False
        else:
            print(f"Drive already mounted at {mount}")
            return True
    else:
        print(f"Mounting not supported on {current_os}, skipping...")
        return False