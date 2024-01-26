# backup_script.py
import subprocess
import os
from datetime import datetime
from backup_config import backup_config

def run_docker_command(container_name, backup_filename, volume_path):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"{backup_filename}-{timestamp}.tar"

    try:
        subprocess.run(f"docker run --rm --volumes-from {container_name} -v /backup:/backup ubuntu tar cf /backup/{backup_file} {volume_path}", check=True, shell=True)
        print(f"Backup for {container_name} successful. Backup saved in: /backup/{backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup for {container_name} failed. Error: {e}")

if __name__ == "__main__":
    for container_name, backup_filename, volume_path in backup_config:
        run_docker_command(container_name, backup_filename, volume_path)