import os
import datetime
import subprocess
import argparse

def clear_old_files(folder_path, days_to_keep):
    current_time = datetime.datetime.now()
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is older than the specified days_to_keep
        if os.path.isfile(file_path):
            last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            age = current_time - last_modified_time
            if age.days > days_to_keep:
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")

def run_docker_backup(command):
    try:
        subprocess.run(command, check=True, shell=True)
        print("Backup command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing backup command: {e}")

def get_backup_folder_and_days(backup_frequency):
    if backup_frequency == "daily":
        folder_path = "/backup/daily"
        days_to_keep = 7
    elif backup_frequency == "weekly":
        folder_path = "/backup/weekly"
        days_to_keep = 31
    elif backup_frequency == "monthly":
        folder_path = "/backup/monthly"
        days_to_keep = 365
    elif backup_frequency == "yearly":
        folder_path = "/backup/yearly"
        days_to_keep = 1825
    else:
        raise ValueError("Invalid backup frequency. Supported values: daily, weekly, monthly, yearly")
    
    return folder_path, days_to_keep

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run Docker backup with different frequencies.")
    parser.add_argument("backup_frequency", choices=["daily", "weekly", "monthly", "yearly"], help="Backup frequency")
    args = parser.parse_args()
    
    # Get folder path and days to keep based on the backup frequency
    folder_path, days_to_keep = get_backup_folder_and_days(args.backup_frequency)
    
    # Clear out old files
    clear_old_files(folder_path, days_to_keep)
    
    # Run the docker_vol_backup.py command
    backup_command = f"python3 docker_vol_backup.py {folder_path}"
    run_docker_backup(backup_command)
