import os
import pyfiglet
import csv
import config
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_FILES_DIR = os.path.join(BASE_DIR, "score_files")
RANDOM_JOB = f"{config.zos_id}.JCL(RNDQTJOB)"

def show_additional_info():
    """
    Displays additional information below the title:
    - Date: current date
    - Logged in: z/OS ID
    - Total score: retrieved from the score document
    """
    # Current date
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Retrieve total score from score.csv
    total_score = 0
    score_file = os.path.join(SCORE_FILES_DIR, "score.csv")  # Correct location of score.csv
    # Check if the file exists and is not empty
    if os.path.exists(score_file) and os.path.getsize(score_file) > 0:
        with open(score_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:  # Ensure the row has at least two elements
                    try:
                        total_score += int(row[1])
                    except ValueError:
                        pass  # Skip rows with invalid data

    # Print additional information
    print("=" * 25)
    print(f"Date:{current_date.rjust(20)}")
    print(f"Logged in:{config.zos_id.rjust(15)}")
    print(f"Total score:{str(total_score).rjust(13)}")
    print("=" * 25)
    print()
    
def execute_jcl_job():
    """
    Executes the JCL job that runs the REXX script.
    """
    zos_id = config.zos_id
    jcl_job_name = "RNDQTJOB"
    
    # Submit the job via Zowe CLI
    submit_command = f"zowe zos-jobs submit local-file '{INSTALL_FILES_DIR}/RUNRANDOMQUOTEREXX.JCL'"
    
    try:
        result = subprocess.run(submit_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92mJCL job '{jcl_job_name}' successfully executed.\033[0m")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError executing JCL job '{jcl_job_name}'.\033[0m")
        print(e.stderr)

def show_title(*titles, additional=True):
    """
    Displays one or more titles in pyfiglet format with empty lines in between.
    Displays additional information afterward.
    """
    for title in titles:
        print(pyfiglet.figlet_format(title))
        print()  # Empty line between titles
    
    # Call show_additional_info once after all titles
    if additional:
        show_additional_info()

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def start_job_randomquote():
    """
    Executes a JCL job to run the RANDOMQT JCL and displays a message upon success.
    """
    # Command to submit the job
    random_command = f'zowe zos-jobs submit data-set "{RANDOM_JOB}"'
    
    try:
        # Execute the submit command
        result = subprocess.run(random_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92mJob {RANDOM_JOB} submitted successfully.\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError submitting job {RANDOM_JOB}.\033[0m")
        print(e.stderr)
        input("Press any key to exit the program.")
