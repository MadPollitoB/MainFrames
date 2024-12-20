import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_FILES_DIR = os.path.join(BASE_DIR, "score_files")

# Function to save the score in score.csv
def update_score(category, action, added_score):
    score_file = os.path.join(SCORE_FILES_DIR, "score.csv")
    try:
        with open(score_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            # Check if category already exists
            category_found = False
            for row in rows:
                if row[0] == category:
                    row[1] = str(int(row[1]) + added_score)  # Update the score
                    category_found = True
                    break
            
            # If category does not exist, add a new category
            if not category_found:
                rows.append([category, str(added_score)])

        # Write the updated rows back to the file
        with open(score_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    except FileNotFoundError:
        # If file doesn't exist, create it and add the category
        with open(score_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["category", "score"])  # Add header
            writer.writerow([category, added_score])

    # Log the score change
    log_score_change(category, action, added_score)

# Function to update logscore.csv with a timestamp
def log_score_change(category, action, added_score):
    log_file = os.path.join(SCORE_FILES_DIR, "logscore.csv")
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    new_row = [current_time, category, action, added_score]

    try:
        # Read the existing content of logscore.csv
        with open(log_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Insert the new row at the top of the list
        rows.insert(0, new_row)

        # Write the updated content back to the file
        with open(log_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    except FileNotFoundError:
        # If the file doesn't exist, create it and add the first row
        with open(log_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["datetime", "category", "action", "added_score"])  # Add header
            writer.writerow(new_row)  # Add the first log row

# Function to display the current score
def show_score():
    score_file = os.path.join(SCORE_FILES_DIR, "score.csv")
    try:
        with open(score_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            print(f"\033[92m{'Category':<20}{'Score':<10}\033[0m")
            print("=" * 30)
            for row in reader:
                print(f"{row[0]:<20}{row[1]:<10}")
    except FileNotFoundError:
        print("\033[91mNo score data found.\033[0m")

# Function to display score logging
def show_score_logging():
    log_file = os.path.join(SCORE_FILES_DIR, "logscore.csv")
    try:
        with open(log_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            print(f"\033[92m{'Date and Time':<25}{'Category':<20}{'Action':<15}{'Added Score'}\033[0m")
            print("=" * 71)
            for row in reader:
                print(f"{row[0]:<25}{row[1]:<20}{row[2]:<15}{row[3]:>5}")
    except FileNotFoundError:
        print("\033[91mNo log data found.\033[0m")

# Function to reset scores
def reset_scores(message=True):
    score_file = os.path.join(SCORE_FILES_DIR, "score.csv")
    log_file = os.path.join(SCORE_FILES_DIR, "logscore.csv")
    
    confirm='y'

    while True:
        if message:
            confirm = input("Are you sure you want to reset the scores? This will delete the score files. (y/n): ").strip().lower()

        if confirm == 'y':
            # Delete the existing files
            if os.path.exists(score_file):
                os.remove(score_file)
                if message:
                    print("\033[92mscore.csv file has been deleted.\033[0m")
            
            if os.path.exists(log_file):
                os.remove(log_file)
                if message:
                    print("\033[92mlogscore.csv file has been deleted.\033[0m")

            # Recreate the files with proper headers
            with open(score_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
            if message:
                print("\033[92mscore.csv file has been recreated.\033[0m")

            with open(log_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
            if message:
                print("\033[92mlogscore.csv file has been recreated.\033[0m")

            break

        elif confirm == 'n':
            print("\033[93mScore reset has been canceled.\033[0m")
            break

        else:
            print("\033[91mInvalid choice. Enter 'y' to reset the scores or 'n' to cancel the action.\033[0m")
