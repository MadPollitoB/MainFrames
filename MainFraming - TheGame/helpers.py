import os
import pyfiglet
import csv
import config
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_FILES_DIR = os.path.join(BASE_DIR, "score_files")
RANDOM_JOB=f"{config.zos_id}.JCL(RNDQTJOB)"

def show_additional_info():
    """
    Toont extra informatie onder de titel:
    - Datum: huidige datum
    - Ingelogd: z/OS ID
    - Totale score: opgehaald uit het score-document
    """
    # Huidige datum
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Totale score ophalen uit score.csv
    total_score = 0
    score_file = os.path.join(SCORE_FILES_DIR, "score.csv")  # Correcte locatie van score.csv
    if os.path.exists(score_file):
        with open(score_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            # next(reader, None)  # Sla de header over
            for row in reader:
                total_score += int(row[1])

    # Print de extra informatie
    print("=" * 25)
    print(f"Datum:{current_date.rjust(19)}")
    print(f"Ingelogd:{config.zos_id.rjust(16)}")
    print(f"Totale score:{str(total_score).rjust(12)}")
    print("=" * 25)
    print()
    
def execute_jcl_job():
    """
    Execute the JCL job that runs the REXX script.
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

def show_title(*titles):
    """
    Toont een of meerdere titels in pyfiglet-formaat onder elkaar met lege lijnen ertussen.
    Toont daarna aanvullende informatie.
    """
    for title in titles:
        print(pyfiglet.figlet_format(title))
        print()  # Lege lijn ertussen
    
    # Roep show_additional_info één keer aan na alle titels
    show_additional_info()

def clear_screen():
    """Clears the console scherm."""
    os.system('cls' if os.name == 'nt' else 'clear')

def start_job_randomquote():
    """
    Voert een JCL job uit om de RANDOMQT JCL te runnen, 
    en toont een bericht als de job succesvol is uitgevoerd.
    """
    # Command voor het submitten van de job
    random_command = f'zowe zos-jobs submit data-set "{RANDOM_JOB}"'
    
    try:
        # Voer het submit commando uit
        result = subprocess.run(random_command, shell=True, check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:
        print(f"\033[91mFout bij het submitten van de job {RANDOM_JOB}).\033[0m")
        print(e.stderr)
        input("Druk op een knop om het programma af te sluiten.")