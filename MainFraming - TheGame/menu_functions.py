import subprocess
import os
import sys
from helpers import (
    show_title, 
    clear_screen, 
    start_job_randomquote
)
from datasets_functions import (
    list_all_datasets,
    create_dataset,
    delete_dataset,
    create_new_dataset,
    download_scores,
    upload_scores,
    list_numeric_datasets,
)
from files_functions import (
    list_all_uss_files, 
    download_files,
    upload_files_to_backup,
    delete_files_from_backup
)
from score import (
    show_score, 
    show_score_logging, 
    reset_scores,
    update_score
)
import config


def delete_local_file(local_file):
    """
    Deletes the specified file if it exists.
    """
    os.remove(local_file)

def get_quote_of_the_moment():
    """
    Retrieves the quote of the moment from the dataset, returns it,
    and deletes the file after use.
    """
    # Set the fixed z/OS dataset name
    dataset_name = f"{config.zos_id}.QUOTES.MOMENT"
    local_file = "downloaded_quotes_moment.txt"

    # Zowe CLI command to fetch the quote of the moment by downloading the dataset
    command = f"zowe zos-files download data-set '{dataset_name}' --file {local_file}"

    try:
        # Execute the download command
        subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError downloading dataset {dataset_name}.\033[0m")
        print(e.stderr)
        # Delete the file if it was created during an erroneous attempt
        delete_local_file(local_file)
        return "No quote available."

    # Read the contents of the downloaded file
    lines = []  # Initialize 'lines' as an empty list
    if os.path.exists(local_file):
        with open(local_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

    # Delete the file after reading or if an error occurred
    delete_local_file(local_file)

    # Check if there are lines in the file and return the first line as the quote
    if len(lines) > 0:
        quote_of_the_moment = lines[0].strip()
    else:
        quote_of_the_moment = "No quote available."

    return quote_of_the_moment

def main_menu(quoterandomise=True):
    """Displays the main menu."""
    clear_screen()
    show_title('MainFraming', 'The Game')
  
    if quoterandomise:
        start_job_randomquote()

    # Retrieve the quote of the moment
    quote = get_quote_of_the_moment()
    line_width = len(quote) + 4

    sys.stdout.write("\033[F")  # Move the cursor up one line
    sys.stdout.write("\033[K")  # Clear the entire line
    sys.stdout.flush()
    
    print("*" * line_width)
    print(f"* {quote.center(len(quote))} *")
    print("*" * line_width)
    print()

    # Print main menu
    print("Main Menu")
    print("=" * 9)
    print("1. DataSets")
    print("2. Files")
    print("3. Score")
    print("4. Change Quote")
    print("5. Exit")

    choice = input("Make a choice: ")
    if choice == '1':
        datasets_menu()
    elif choice == '2':
        files_menu()
    elif choice == '3':
        score_menu()
    elif choice == '4':
        update_score("quotes", "get", 5)
        main_menu(True)
    elif choice == '5':
        exit_app()
    else:
        print("\033[91m\nInvalid choice. Try again.\033[0m")
        input("Press Enter to continue...")
        main_menu()

def datasets_menu():
    """Displays the DataSets menu."""
    clear_screen()
    show_title('DataSets')
    
    print("=" * 24)
    print("1. Show all Datasets")
    print("2. Create Dataset")
    print("3. Delete Dataset")
    print("4. Return to Main Menu")
    print("5. Exit")

    choice = input("Make a choice: ")
    if choice == '1':
        list_all_datasets(navigate_back=datasets_menu) 
    elif choice == '2':
        create_new_dataset(navigate_back=datasets_menu)
    elif choice == '3':
        delete_dataset(navigate_back=datasets_menu)
    elif choice == '4':
        main_menu()
    elif choice == '5':
        exit_app()
    else:
        print("\033[91m\nInvalid choice. Try again.\033[0m")
        input("Press Enter to continue...")
        datasets_menu()

def files_menu():
    """Displays the Files menu."""
    clear_screen()
    show_title('Files')
    
    print("=" * 24)
    print("1. Show all Files in Backup")
    print("2. Send File to Backup")
    print("3. Download Files from Backup")
    print("4. Remove Files from Backup")
    print("5. Return to Main Menu")
    print("6. Exit")

    choice = input("Make a choice: ")
    if choice == '1':
        list_all_uss_files(navigate_back=files_menu)
    elif choice == '2':
        upload_files_to_backup(navigate_back=files_menu)
    elif choice == '3':
        download_files(navigate_back=files_menu)
    elif choice == '4':
        delete_files_from_backup(navigate_back=files_menu)
    elif choice == '5':
        main_menu()
    elif choice == '6':
        exit_app()
    else:
        print("\033[91m\nInvalid choice. Try again.\033[0m")
        input("Press Enter to continue...")
        datasets_menu()

def score_menu():
    """Displays the Score menu."""
    clear_screen()
    show_title('Score Menu')
    print("Choose from the following options:")
    print("=" * 24)
    print("1. Show Score")
    print("2. Show Score Logging")
    print("3. Reset Scores")
    print("4. Download Scores from Mainframe")
    print("5. Upload Scores to Mainframe")
    print("6. Return to Main Menu")
    print("7. Exit")

    choice = input("Make a choice: ")
    if choice == '1':
        print()
        show_score()  # Show current score
        input("\nPress Enter to continue...")
        score_menu()
    elif choice == '2':
        print()
        show_score_logging()  # Show score log
        input("\nPress Enter to continue...")
        score_menu()
    elif choice == '3':
        print()
        reset_scores()
        input("\nPress Enter to continue...")
        score_menu()
    elif choice == '4':
        print()
        download_scores()
        input("\nPress Enter to continue...")
        score_menu()
    elif choice == '5':
        print()
        upload_scores()
        input("\nPress Enter to continue...")
        score_menu()
    elif choice == '6':
        main_menu()
    elif choice == '7':
        exit_app()
    else:
        print("\033[91m\nInvalid choice. Try again.\033[0m")
        input("Press Enter to continue...")
        score_menu()

def exit_app():
    """Closes the application."""
    print("\033[93mApplication is closing.\033[0m")
    exit()
