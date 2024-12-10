import subprocess
import re
import os
import csv  # Make sure csv is imported
import importlib


# Check if config file exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_FILES_DIR = os.path.join(BASE_DIR, "install_files")
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config.py")

# If config.py does not exist -> create it
if not os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, "w") as config_file:
        config_file.write("zos_id = ''")

# Import extra libraries
import config
from datasets_functions import create_dataset, check_dataset_exists
from helpers import clear_screen

# Functions
def get_valid_zos_id():
    """Prompt the user for a valid zOS ID until the correct format is provided."""
    errorshow = False
    error = "\033[91mInvalid input. The z/OS ID must be in the format 'zXXXXX', where 'X' is a digit.\033[0m"
    zos_id_pattern = r'^z\d{5}$'  # Regex for format "zXXXXX" where X is a digit.

    while True:
        clear_screen()
        if errorshow:
            print(f"{error}")

        zos_id = input("Please enter your z/OS ID in the format 'zXXXXX' (e.g., z12345): ").strip()
        if re.match(zos_id_pattern, zos_id):
            return zos_id
        else: 
            errorshow = True

def update_or_add_zos_id(zos_id):
    """Update or add the zOS ID to the config file."""
    zos_id_cap = zos_id.upper()

    # Prepare the lines to write in config.py
    new_lines = []
    zos_id_exists = False
    zos_id_cap_exists = False

    # Read current config content
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as file:
            lines = file.readlines()
        
        # Modify lines if necessary
        for line in lines:
            if line.startswith('zos_id ='):
                new_lines.append(f"zos_id = '{zos_id}'\n")
                zos_id_exists = True
            elif line.startswith('zos_id_cap ='):
                new_lines.append(f"zos_id_cap = '{zos_id_cap}'\n")
                zos_id_cap_exists = True
            else:
                new_lines.append(line)

    # Add zos_id and zos_id_cap if they don't exist
    if not zos_id_exists:
        new_lines.append(f"zos_id = '{zos_id}'\n")
    if not zos_id_cap_exists:
        new_lines.append(f"zos_id_cap = '{zos_id_cap}'\n")

    # Write the updated config content back to the file
    with open(CONFIG_FILE_PATH, 'w') as file:
        file.writelines(new_lines)

    print(f"zOS ID saved successfully: zos_id = '{zos_id}', zos_id_cap = '{zos_id_cap}'")

    # Re-import the config file
    print("Importing the latest config file")
    importlib.reload(config)

# Function to install all required dependencies
def install_dependencies():
    """Install all required dependencies."""
    dependencies = ['pyfiglet', 'requests']
    for dependency in dependencies:
        try:
            importlib.import_module(dependency)
        except ImportError:
            print(f"Dependency {dependency} is not installed. Installing...")
            subprocess.check_call(['pip', 'install', dependency])

# Function to normalize a quote
def normalize_quote(quote):
    # Replace typographic quotes with standard quotes
    quote = quote.replace("’", "'").replace("‘", "'").replace("“", "\"").replace("”", "\"")
    # Remove other special characters
    quote = quote.replace("`", "'").replace(".", "")
    # Limit length
    max_length = 200
    if len(quote) > max_length:
        quote = quote[:max_length]
    return quote

def create_score_files():
    # Define the directory and file paths
    directory = "score_files"
    file_path = os.path.join(directory, "score.csv")
    log_file_path = os.path.join(directory, "logscore.csv")

    # Create the directory if it does not exist
    os.makedirs(directory, exist_ok=True)

    # Create score.txt if it does not exist
    if not os.path.exists(file_path):
        # Create an empty text file
        with open(file_path, "w") as score_file:
            pass  # Leave the file empty
        print(f"\033[92mCreated {file_path}\033[0m")
    else:
        print(f"\033[93m{file_path} already exists.\033[0m")

    # Create logscore.txt if it does not exist
    if not os.path.exists(log_file_path):
        # Create an empty text file
        with open(log_file_path, "w") as log_file:
            pass  # Leave the file empty
        print(f"\033[92mCreated {log_file_path}\033[0m")
    else:
        print(f"\033[93m{log_file_path} already exists.\033[0m")

# Function to normalize quotes in quotes.csv
def normalize_quotes_file(quotes_file):
    """Normalize all quotes in the quotes.csv file."""
    if not os.path.exists(quotes_file):
        print(f"\033[91m{quotes_file} not found. Verify the file exists.\033[0m")
        return

    normalized_quotes = []
    try:
        with open(quotes_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    quote = row[0]
                    normalized_quote = normalize_quote(quote)
                    normalized_quotes.append([normalized_quote])
        
        with open(quotes_file, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(normalized_quotes)

        print(f"\033[92mAll quotes in {quotes_file} were successfully normalized.\033[0m")
    except Exception as e:
        print(f"\033[91mError normalizing the file {quotes_file}: {e}\033[0m")

# Function to create the QUOTES and QUOTE.MOMENT datasets
def check_and_create_quotes_dataset():
    zos_id = config.zos_id
    dataset_name = f"{zos_id}.QUOTES"
    moment_dataset_name = f"{zos_id}.QUOTES.MOMENT"
    quotes_file = os.path.join(INSTALL_FILES_DIR, "quotes.csv")

    normalize_quotes_file(quotes_file)

    if not check_dataset_exists(dataset_name):
        create_dataset(dataset_name, dataset_type="seq")

    if not check_dataset_exists(moment_dataset_name):
        create_dataset(moment_dataset_name, dataset_type="seq")

    if not os.path.exists(quotes_file):
        print(f"\033[91m{quotes_file} not found. Verify the file exists.\033[0m")
        return

    upload_command = f"zowe zos-files upload file-to-data-set \"{quotes_file}\" \"{dataset_name}\""
    try:
        subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92m{quotes_file} successfully uploaded to {dataset_name}\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError uploading {quotes_file} to {dataset_name}.\033[0m")
        print(e.stderr)

# Function to upload REXX script to mainframe
def upload_rexx_script_to_mainframe():
    zos_id = config.zos_id
    rexx_dataset = f"{zos_id}.REXX"
    rexx_file = os.path.abspath(os.path.join(INSTALL_FILES_DIR, "RANDOMQUOTE.REXX"))
    print(f"Searching for REXX file at: {rexx_file}")

    create_dataset(rexx_dataset, dataset_type="pds")

    upload_command = f'zowe zos-files upload file-to-data-set "{rexx_file}" "{rexx_dataset}(RANDOMQT)"'
    try:
        subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92m{rexx_file} successfully uploaded to {rexx_dataset}(RANDOMQT).\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError uploading {rexx_file} to {rexx_dataset}(RANDOMQT).\033[0m")
        print(e.stderr)

# Function to upload JCL job
def upload_jcl_to_mainframe():
    zos_id = config.zos_id
    jcl_dataset = f"{zos_id}.JCL"
    member = "RNDQTJOB"
    jcl_file = os.path.abspath(os.path.join(INSTALL_FILES_DIR, "RUNRNDQT.JCL"))
    print(f"Searching for JCL file at: {jcl_file}")

    create_dataset(jcl_dataset, dataset_type="pds")

    upload_command = f'zowe zos-files upload file-to-data-set "{jcl_file}" "{jcl_dataset}({member})"'
    try:
        subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92m{jcl_file} successfully uploaded to {jcl_dataset}({member}).\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError uploading {jcl_file} to {jcl_dataset}({member}).\033[0m")
        print(e.stderr)

    # Download the file to verify the content
    download_file = "downloaded_member.txt"
    download_command = f'zowe zos-files download data-set "{jcl_dataset}({member})" --file "{download_file}"'
    subprocess.run(download_command, shell=True, check=True, capture_output=True, text=True)

    # Verify that the file is as expected
    if os.path.exists(download_file):
        with open(download_file, "r") as f_downloaded:
            downloaded_content = f_downloaded.read().strip()

        if downloaded_content != "":
            print(f"\033[92mThe file {jcl_dataset}({member}) was successfully populated.\033[0m")
        else:
            print(f"\033[91mThe file {jcl_dataset}({member}) is empty. QUOTES will not work.\033[0m")
    else:
        print(f"\033[91mError downloading {jcl_dataset}({member}). File not found.\033[0m")

    # Remove the downloaded file after verification
    if os.path.exists(download_file):
        os.remove(download_file)

def check_and_create_backup_folder(folder_path):
    """
    Check if the backup folder in the USS exists and create it if needed.
    """
    # Zowe CLI command to check if the folder exists
    check_command = f"zowe zos-files list uss-files {folder_path}"
    
    try:
        # Check if the folder exists
        subprocess.run(check_command, shell=True, capture_output=True, text=True, check=True)
        print(f"\033[93mBackup folder already exists: {folder_path}\033[0m")
    except subprocess.CalledProcessError:
        # If the folder path does not exist, create it
        print(f"\033[93mBackup folder does not exist. Creating...\033[0m")
        create_command = f"zowe zos-files create uss-directory {folder_path}"
        try:
            subprocess.run(create_command, shell=True, capture_output=True, text=True, check=True)
            print(f"\033[92mBackup folder successfully created: {folder_path}\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[91mError creating the backup folder:\033[0m {e.stderr}")
        except Exception as e:
            print(f"\033[91mUnexpected error occurred while creating the backup folder:\033[0m {str(e)}")

def update_backup_config():
    zos_id = config.zos_id
    backup_folder_name = 'backups'
    restore_folder_name = 'backups_restore'

    """
    Update or add the USS backup folder and local restore folder to the config file.
    """
    # Get current directory
    current_dir = os.getcwd()

    # Full path to the local restore folder
    restore_folder_path = os.path.join(current_dir, restore_folder_name)

    # Check if the local restore folder exists
    if not os.path.exists(restore_folder_path):
        # Create the folder
        os.makedirs(restore_folder_path)
        print(f"\033[92mLocal restore folder created: {restore_folder_path}\033[0m")  # Green text
    else:
        print(f"\033[93mLocal restore folder already exists: {restore_folder_path}\033[0m")  # Yellow text

    # Lines to be written in the config file
    backup_folder_line = f"uss_backup_folder = '/z/{zos_id}/{backup_folder_name}'\n"
    restore_folder_line = f"local_restore_folder = '{restore_folder_name}'\n"

    # New lines for the config file
    new_lines = []
    backup_folder_exists = False
    restore_folder_exists = False

    # Read the existing config file
    with open(CONFIG_FILE_PATH, 'r') as file:
        lines = file.readlines()

    # Check if the 'uss_backup_folder' and 'local_restore_folder' lines already exist
    for line in lines:
        if line.startswith('uss_backup_folder ='):
            new_lines.append(backup_folder_line)  # Update the backup line
            backup_folder_exists = True
        elif line.startswith('local_restore_folder ='):
            new_lines.append(restore_folder_line)  # Update the restore line
            restore_folder_exists = True
        else:
            new_lines.append(line)

    # If the lines do not exist, add them
    if not backup_folder_exists:
        new_lines.append(backup_folder_line)
    if not restore_folder_exists:
        new_lines.append(restore_folder_line)

    # Write the updated lines back to the config file
    with open(CONFIG_FILE_PATH, 'w') as file:
        file.writelines(new_lines)

    print(f"\033[92mUSS Backup folder set to: /z/{zos_id}/{backup_folder_name}\033[0m")
    print(f"\033[92mLocal restore folder set to: {restore_folder_path}\033[0m")

    # Ensure backup folder exists on USS
    check_and_create_backup_folder(f'/z/{zos_id}/{backup_folder_name}')