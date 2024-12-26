import subprocess
import importlib
from install import (
    create_score_files,
    check_and_create_quotes_dataset,
    install_dependencies,
    upload_rexx_script_to_mainframe,
    upload_jcl_to_mainframe,
    get_valid_zos_id,
    update_or_add_zos_id,
    update_backup_config
)
from menu_functions import main_menu
from cheating import check_cheating
import os

# Define paths for score and log files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_FILES_DIR = os.path.join(BASE_DIR, "score_files")
score_file = os.path.join(SCORE_FILES_DIR, "score.csv")
log_file = os.path.join(SCORE_FILES_DIR, "logscore.csv")

def main():
    print("\033[96mChecking and installing required dependencies, datasets, and mainframe files!\033[0m")
    print("\033[96mPlease wait...\033[0m")
    print()

    # Prompt for IBM login credentials
    # Get valid zOS ID from the user
    zos_id = get_valid_zos_id()

    # Update or add the zOS ID in config.py
    update_or_add_zos_id(zos_id)
    
    # Check or update the backup folders
    update_backup_config()

    # Install dependencies if not already installed
    install_dependencies()
    
    # Create and verify if the quotes dataset exists on the mainframe
    check_and_create_quotes_dataset()
    
    # Check score environment
    create_score_files()

    # Upload the JCL and REXX script to the mainframe
    upload_rexx_script_to_mainframe()  # Upload the REXX script
    upload_jcl_to_mainframe()  # Upload the JCL script

    input("\nPress Enter to start the program.")
   
    check_cheating(score_file, log_file)
    
    main_menu(True)

if __name__ == "__main__":
    main()
