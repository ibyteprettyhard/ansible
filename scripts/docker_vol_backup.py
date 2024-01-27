# import subprocess
# from datetime import datetime
# from os.path import join, abspath, dirname
# from backup_config import backup_config

# def run_docker_command(container_name, backup_filename, volume_path, exclude_file=None):
#     timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
#     backup_file = f"{timestamp}--{backup_filename}.tar"
#     backup_location = "/backup/"

#     exclude_option = ""
#     if exclude_file:
#         # Construct the absolute path to the exclude file
#         exclude_file_path = abspath(join(dirname(__file__), exclude_file))
#         with open(exclude_file_path, 'r') as file:
#             exclude_content = file.read().strip()
#             exclude_option = ' '.join(f'--exclude={line.strip()}' for line in exclude_content.splitlines())

#     try:
#         command = f"docker run --rm --volumes-from {container_name} -v {backup_location}:/backup ubuntu tar {exclude_option} -cf {backup_location}{backup_file} {volume_path}"
#         print(f"Running command: {command}")
#         subprocess.run(command, check=True, shell=True)
#         print(f"Backup for {container_name} successful. Backup saved in: {backup_location}{backup_file}")
#     except subprocess.CalledProcessError as e:
#         print(f"Backup for {container_name} failed. Error: {e}")

# if __name__ == "__main__":
#     for container_name, backup_filename, volume_path, exclude_file in backup_config:
#         run_docker_command(container_name, backup_filename, volume_path, exclude_file)
import subprocess
from datetime import datetime
from os.path import join, abspath, dirname
from backup_config import backup_config
import argparse

def run_docker_command(container_name, backup_filename, volume_path, backup_location, exclude_file=None):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    backup_file = f"{timestamp}--{backup_filename}.tar"
    target_backup_location = "/backup/"

    exclude_option = ""
    if exclude_file:
        # Construct the absolute path to the exclude file
        exclude_file_path = abspath(join(dirname(__file__), exclude_file))
        with open(exclude_file_path, 'r') as file:
            exclude_content = file.read().strip()
            exclude_option = ' '.join(f'--exclude={line.strip()}' for line in exclude_content.splitlines())

    try:
        # Ensure the target backup directory exists within the Docker container
        subprocess.run(f"docker run --rm --volumes-from {container_name} -v {backup_location}:/backup ubuntu mkdir -p {target_backup_location}", check=True, shell=True)

        # Run the tar command to create the backup
        command = f"docker run --rm --volumes-from {container_name} -v {backup_location}:/backup ubuntu tar {exclude_option} -cf {target_backup_location}{backup_file} {volume_path}"
        print(f"Running command: {command}")
        subprocess.run(command, check=True, shell=True)
        print(f"Backup for {container_name} successful. Backup saved in: {target_backup_location}{backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup for {container_name} failed. Error: {e}")

def main():
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description="Run Docker backup commands for specified containers.")
    parser.add_argument("backup_location", help="Path to the backup location")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the run_docker_command function for each entry in backup_config
    for container_name, backup_filename, volume_path, exclude_file in backup_config:
        run_docker_command(container_name, backup_filename, volume_path, args.backup_location, exclude_file)

if __name__ == "__main__":
    main()

