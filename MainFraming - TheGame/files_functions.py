import re
import os
import subprocess
from score import update_score
import config
from helpers import show_title, clear_screen

def list_all_uss_files(navigate_back, message=""):
    """
    Retrieves all files in the USS backup folder using Zowe CLI, 
    based on the USS path from config.cfg.
    
    The score is updated only if the files are successfully retrieved.
    """
    clear_screen()
    show_title("USS Backup Files")

    if message != "":
        print(f"\033[92m{message}\033[0m\n")

    uss_backup_folder = config.uss_backup_folder

    # Build the Zowe CLI command
    list_command = f"zowe zos-files list uss-files {uss_backup_folder}"

    try:
        # Execute the Zowe CLI command
        list_files = subprocess.run(list_command, shell=True, capture_output=True, text=True, check=True)

        # Decode the output
        files = list_files.stdout.splitlines()  # Split the output into individual lines

        # Use regex to extract full filenames, including spaces
        files_and_types = []
        for line in files:
            # Regex to separate name and type
            match = re.match(r'^(.+?)\s+(-[rwx-]+)\s+', line)
            if match:
                files_and_types.append(f"{match.group(1)}")

        # Display the files
        print("Available files in the USS backup folder:")
        print("=" * 45)
        if files_and_types:
            for file in files_and_types:
                print(file)
        else:
            print("\033[93mNo files found in the backup folder.\033[0m")

        # Update the score only if the files were successfully retrieved
        update_score("files", "list", 1)

    except subprocess.CalledProcessError as e:
        print("\033[91m\nError retrieving files from USS:\033[0m")
        print(e.stderr)
    except Exception as e:
        print("\033[91m\nUnexpected error occurred:\033[0m")
        print(str(e))

    input("\nPress Enter to go back.")

    # Use the callback to navigate back
    navigate_back()

def upload_files_to_backup(navigate_back):
    """
    Uploads files to the USS backup folder using Zowe CLI.
    Adds 5 points for successful uploads and displays a success message.
    """
    clear_screen()
    show_title("Upload Files to USS Backup")

    while True:
        # Prompt for a file path
        file_path = input("Enter the full path of the file to upload (or 'q' to go back): ").strip()

        # Check if the user wants to go back to the menu
        if file_path.lower() == 'q':
            print("Returning to the menu...")
            navigate_back()
            return

        # Check if the file exists
        if not os.path.isfile(file_path):
            print("\033[91m\nThe specified file does not exist. Please try again.\033[0m")
            continue

        # Validate the file name
        file_name = os.path.basename(file_path)
        if not re.match(r"^[a-zA-Z0-9_.\-\s]+$", file_name):
            print("\033[91m\nInvalid file name. Use only letters, numbers, spaces, underscores, or dashes.\033[0m")
            continue

        # Build the Zowe CLI command for upload
        uss_backup_folder = config.uss_backup_folder
        destination_path = f"{uss_backup_folder}/{file_name}"
        upload_command = f'zowe zos-files upload file-to-uss "{file_path}" "{destination_path}" --binary'

        try:
            # Execute the upload command
            subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)
            print(f"\033[92m File uploaded successfully: {file_path} to {destination_path}\033[0m")

            # Add points and display success message
            update_score("files", "upload", 5)
            print("5 points added for the upload.\n")

        except subprocess.CalledProcessError as e:
            print(f"\033[91m Error uploading file: {e.stderr}\033[0m")
            continue

        # Ask if the user wants to upload another file
        proceed = input("Do you want to upload another file? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Returning to the menu...")
            navigate_back()
            return