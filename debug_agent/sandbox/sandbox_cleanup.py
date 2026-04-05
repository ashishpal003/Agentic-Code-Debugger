import os
import shutil
import time

def cleanup_old_sandboxes(tmp_dir="/private/var/folders/n8/j0_rrlzd54b4xk3yllh67k000000gn/T", prefix="debug_agent_", max_age_hours=6):
    now = time.time()

    for folder in os.listdir(tmp_dir):
        if folder.startswith(prefix):
            full_path = os.path.join(tmp_dir, folder)
            
            if os.path.isdir(full_path):
                creation_time = os.path.getctime(full_path)
                age_hours = (now - creation_time) / 3600

                if age_hours > max_age_hours:
                    shutil.rmtree(full_path)