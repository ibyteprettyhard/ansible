# backup_script.py
import subprocess
from datetime import datetime
from os.path import join, abspath, dirname
from backup_config import backup_config

def run_docker_command(container_name, backup_filename, volume_path, exclude_file=None):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"{backup_filename}-{timestamp}.tar"
    backup_location = "/backup/"

    exclude_option = ""
    if exclude_file:
        # Construct the absolute path to the exclude file
        exclude_file_path = abspath(join(dirname(__file__), exclude_file))
        with open(exclude_file_path, 'r') as file:
            exclude_content = file.read().strip()
            exclude_option = ' '.join(f'--exclude={line.strip()}' for line in exclude_content.splitlines())

    try:
        command = f"docker run --rm --volumes-from {container_name} -v {backup_location}:/backup ubuntu tar {exclude_option} -cf {backup_location}{backup_file} {volume_path}"
        print(f"Running command: {command}")
        subprocess.run(command, check=True, shell=True)
        print(f"Backup for {container_name} successful. Backup saved in: {backup_location}{backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup for {container_name} failed. Error: {e}")

if __name__ == "__main__":
    for container_name, backup_filename, volume_path, exclude_file in backup_config:
        run_docker_command(container_name, backup_filename, volume_path, exclude_file)
