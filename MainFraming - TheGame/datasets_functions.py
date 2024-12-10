import re
import os
import subprocess
from helpers import show_title, clear_screen
from score import update_score
import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_FILES_DIR = os.path.join(BASE_DIR, "score_files")

def check_dataset_exists(dataset_name):
    """
    Checks if a dataset exists on the mainframe.
    Returns True if the dataset exists, otherwise False.
    """
    check_command = f"zowe zos-files list ds {dataset_name}"
    try:
        result = subprocess.run(check_command, shell=True, check=True, capture_output=True, text=True)
        # If no error occurs, it means the dataset exists
        if result.stdout.strip():  # If there is output, it means the dataset exists
            return True
    except subprocess.CalledProcessError:
        pass  # No output means the dataset does not exist
    return False

def create_dataset(dataset_name, dataset_type="ds"):
    """
    Creates a dataset if it does not already exist.
    The type can be "ds" for a regular dataset or "pds" for a Partitioned Data Set.
    Use "seq" for sequential datasets.
    """
    # Check if the dataset exists
    if check_dataset_exists(dataset_name):
        print(f"\033[93mDataset {dataset_name} already exists.\033[0m")
    else:
        print(f"\033[96mDataset {dataset_name} does not exist. Creating it...\033[0m")
        
        # Use appropriate options for sequential datasets
        if dataset_type == "seq":
            create_command = f"zowe zos-files create data-set-sequential {dataset_name} --record-format FB --record-length 200 --block-size 800"
        else:
            create_command = f"zowe zos-files create {dataset_type} {dataset_name} --record-format FB --record-length 200 --block-size 800"
        
        try:
            subprocess.run(create_command, shell=True, check=True, capture_output=True, text=True)
            print(f"\033[92mDataset {dataset_name} created successfully.\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[91mError creating dataset {dataset_name}.\033[0m")
            print(e.stderr)

def list_all_datasets(navigate_back, message=""):
    """
    Retrieves all datasets using Zowe CLI, based on the zos_id in config.cfg.
    """
    clear_screen()
    show_title("Zowe Datasets")

    if message != "": 
        print(f"\033[92m{message}\033[0m")
        print()
    else: 
        update_score("datasets", "read", 1)

    # Build the Zowe CLI command
    list_command = f"zowe zos-files list ds {config.zos_id}.*"

    try:
        # Execute the Zowe CLI command
        list_ds = subprocess.run(list_command, shell=True, capture_output=True, text=True, check=True)

        # Decode and display the output
        print("Available DataSets:")
        print("=" * 24)
        print(list_ds.stdout)
    except subprocess.CalledProcessError as e:
        print("\033[91m\nError retrieving datasets:\033[0m")
        print(e.stderr)
    except FileNotFoundError:
        print("\033[91m\nZowe CLI not found. Ensure Zowe CLI is installed and configured.\033[0m")

    input("\nPress Enter to go back.")

    # Use the callback to navigate back
    navigate_back()

def create_new_dataset(navigate_back):
    """
    Creates a dataset using Zowe CLI, based on the zos_id in config.cfg.
    Displays success or error messages.
    """
    clear_screen()
    show_title("Zowe Datasets")

    # Prompt the user for a dataset name
    dataset_name = ""
    while not dataset_name: 
        dataset_name = input("Enter a name for the new dataset: ").strip()

        if not dataset_name:
            print("\033[91m\nNo dataset name provided. Please try again.\033[0m")
        
        if not re.match("^[a-zA-Z0-9]+$", dataset_name):
           print("\033[91m\nInvalid name. Use only letters and numbers.\033[0m")
           dataset_name = ""
    
    dataset_name = dataset_name.lower()

    # Construct the full dataset name
    dataset_name_full = f"{config.zos_id}.{dataset_name}"

    # Create the dataset (use the create_dataset function)
    create_dataset(dataset_name_full, dataset_type="ds")

    # After successfully creating the dataset, display the datasets
    update_score("datasets", "create", 5)
    list_all_datasets(navigate_back, "Dataset created successfully!")

def delete_dataset(navigate_back):
    """
    Deletes a dataset using Zowe CLI.
    First displays a numbered list of datasets for the user to choose from.
    """
    clear_screen()

    show_title("Zowe Datasets")

    datasets = list_numeric_datasets()

    print("q. back to dataset menu")
    
    # Step 3: Ask the user for a choice
    while True:
        choice = input("\nEnter the number of the dataset to delete or 'q' to go back: ").strip().lower()

        if choice == 'q':
            # If the user enters 'q', go back to the dataset menu
            navigate_back()
            return

        try:
            # Try converting the choice to an integer
            choice = int(choice)
            if choice < 1 or choice > len(datasets):
                print("\033[91m\nError: Invalid input! Choose a valid number or 'q' to go back.\033[0m")
            else:
                break  # Exit the loop if the input is valid
        except ValueError:
            # If the input is not a valid number, show an error message
            print("\033[91m\nError: Invalid input! Choose a valid number or 'q' to go back.\033[0m")

    # Step 4: Delete the selected dataset
    dataset_to_delete = datasets[choice - 1]
    delete_command = f"zowe zos-files delete data-set {dataset_to_delete} -f"
    try:
        subprocess.run(delete_command, shell=True, check=True, capture_output=True, text=True)
        update_score("datasets", "delete", 5) 
        list_all_datasets(navigate_back, "Dataset deleted successfully!")

    except subprocess.CalledProcessError as e:
        clear_screen()
        print("\033[91mFailed to delete dataset.\033[0m")
        print(f"\nError details:\n{e.stderr}")
        input("Press Enter to continue.")
        navigate_back()

def download_scores(): 
    zos_id = config.zos_id
    score_dataset = f"{zos_id}.SCORE"
    scorelog_dataset = f"{zos_id}.SCORELOG"

    score_file = os.path.join(SCORE_FILES_DIR, "score.csv")
    log_file = os.path.join(SCORE_FILES_DIR, "logscore.csv")

    # Download the score dataset
    download_command = f'zowe zos-files download data-set "{score_dataset}" --file "{score_file}"'
    try:
        subprocess.run(download_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92mSCORES downloaded successfully.\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError downloading SCORES.\033[0m")
        print(e.stderr)

    # Download the score log dataset
    download_command = f'zowe zos-files download data-set "{scorelog_dataset}" --file "{log_file}"'
    try:
        subprocess.run(download_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92mSCORELOGS downloaded successfully.\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError downloading SCORELOGS.\033[0m")
        print(e.stderr)
    
def upload_scores():
    zos_id = config.zos_id
    score_dataset = f"{zos_id}.SCORE"
    scorelog_dataset = f"{zos_id}.SCORELOG"

    score_file = os.path.join(SCORE_FILES_DIR, "score.csv")
    log_file = os.path.join(SCORE_FILES_DIR, "logscore.csv")
    
    # Upload scores to SCORE
    create_dataset(score_dataset, dataset_type="ds")

    upload_command = f'zowe zos-files upload file-to-data-set "{score_file}" "{score_dataset}"'
    try:
        subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92mSCORES uploaded successfully.\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError uploading SCORES.\033[0m")
        print(e.stderr)
        
    # Upload scores to SCORELOG
    create_dataset(scorelog_dataset, dataset_type="ds")

    upload_command = f'zowe zos-files upload file-to-data-set "{log_file}" "{scorelog_dataset}"'
    try:
        subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92mSCORELOGS uploaded successfully.\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError uploading SCORELOGS.\033[0m")
        print(e.stderr)

def list_numeric_datasets():
    # Step 1: Retrieve all available datasets
    list_command = f"zowe zos-files list ds {config.zos_id}.*"
    try:
        result = subprocess.run(list_command, shell=True, capture_output=True, text=True, check=True)
        datasets = result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        print("\033[91m\nError retrieving datasets:\033[0m")
        print(e.stderr)
        input("\nPress Enter to go back.")
        navigate_back()
        return

    # Check if there are datasets
    if not datasets:
        print("\033[93m\nNo datasets found to delete.\033[0m")
        input("\nPress Enter to go back.")
        navigate_back()
        return

    # Step 2: Display a numbered list of datasets
    print("Available DataSets:")
    for i, dataset in enumerate(datasets, start=1):
        print(f"{i}. {dataset}")

    return datasets
