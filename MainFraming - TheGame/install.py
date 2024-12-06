import subprocess
import re
import os
import csv  # Zorg dat csv is geïmporteerd
import importlib


#check if config file exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_FILES_DIR = os.path.join(BASE_DIR, "install_files")
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config.py")

#indien config.py  niet bestaat -> aanmaken
if not os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, "w") as config_file:
        config_file.write("zos_id = ''")

# oimport extra libraries
import config
from datasets_functions import create_dataset, check_dataset_exists
from helpers import clear_screen

# functions
def get_valid_zos_id():
    """Prompt the user for a valid zOS ID until the correct format is provided."""
    errorshow=False
    error="\033[91mInvalid input. The z/OS ID must be in the format 'zXXXXX', where 'X' is a digit.\033[0m"
    zos_id_pattern = r'^z\d{5}$'  # Regex for format "zXXXXX" where X is a digit.

    while True:
        clear_screen()
        if errorshow:
            print(f"{error}")

        zos_id = input("Please enter your z/OS ID in the format 'zXXXXX' (e.g., z12345): ").strip()
        if re.match(zos_id_pattern, zos_id):
            return zos_id
        else: 
            errorshow=True

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

    #herimporteer de configfiles
    print("Importeer de nieuwste configfile")
    importlib.reload(config)

# Functie om alle benodigde dependencies te installeren
def install_dependencies():
    """Installeer alle vereiste dependencies."""
    dependencies = ['pyfiglet', 'requests']
    for dependency in dependencies:
        try:
            importlib.import_module(dependency)
        except ImportError:
            print(f"Dependency {dependency} is niet geïnstalleerd. Installeren...")
            subprocess.check_call(['pip', 'install', dependency])

# Functie om een quote te normaliseren
def normalize_quote(quote):
    # Vervang typografische aanhalingstekens door standaard aanhalingstekens
    quote = quote.replace("’", "'").replace("‘", "'").replace("“", "\"").replace("”", "\"")
    # Verwijder andere speciale tekens
    quote = quote.replace("`", "'").replace(".", "")
    # Beperk lengte
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
        print(f"Created {file_path}")
    else:
        print(f"{file_path} already exists.")

    # Create logscore.txt if it does not exist
    if not os.path.exists(log_file_path):
        # Create an empty text file
        with open(log_file_path, "w") as log_file:
            pass  # Leave the file empty
        print(f"Created {log_file_path}")
    else:
        print(f"{log_file_path} already exists.")

# Functie om quotes te normaliseren in quotes.csv
def normalize_quotes_file(quotes_file):
    """Normaliseer alle quotes in het quotes.csv bestand."""
    if not os.path.exists(quotes_file):
        print(f"\033[91m{quotes_file} niet gevonden. Controleer of het bestand aanwezig is.\033[0m")
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

        print(f"\033[92mAlle quotes in {quotes_file} zijn succesvol genormaliseerd.\033[0m")
    except Exception as e:
        print(f"\033[91mFout bij het normaliseren van het bestand {quotes_file}: {e}\033[0m")

# Functie om de dataset QUOTES en QUOTE.MOMENT aan te maken
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
        print(f"\033[91m{quotes_file} niet gevonden. Controleer of het bestand aanwezig is.\033[0m")
        return

    upload_command = f"zowe zos-files upload file-to-data-set \"{quotes_file}\" \"{dataset_name}\""
    try:
        subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92m{quotes_file} succesvol geüpload naar {dataset_name}\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mFout bij het uploaden van {quotes_file} naar {dataset_name}.\033[0m")
        print(e.stderr)

# Functie om REXX script te uploaden naar mainframe
def upload_rexx_script_to_mainframe():
    zos_id = config.zos_id
    rexx_dataset = f"{zos_id}.REXX"
    rexx_file = os.path.abspath(os.path.join(INSTALL_FILES_DIR, "RANDOMQUOTE.REXX"))
    print(f"Zoeken naar REXX-bestand op: {rexx_file}")

    create_dataset(rexx_dataset, dataset_type="pds")

    upload_command = f'zowe zos-files upload file-to-data-set "{rexx_file}" "{rexx_dataset}(RANDOMQT)"'
    try:
        subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92m{rexx_file} succesvol geüpload naar {rexx_dataset}(RANDOMQT).\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mFout bij het uploaden van {rexx_file} naar {rexx_dataset}(RANDOMQT).\033[0m")
        print(e.stderr)

# Functie om JCL job te uploaden
def upload_jcl_to_mainframe():
    zos_id = config.zos_id
    jcl_dataset = f"{zos_id}.JCL"
    member = "RNDQTJOB"
    jcl_file = os.path.abspath(os.path.join(INSTALL_FILES_DIR, "RUNRNDQT.JCL"))
    print(f"Zoeken naar JCL-bestand op: {jcl_file}")

    create_dataset(jcl_dataset, dataset_type="pds")

    upload_command = f'zowe zos-files upload file-to-data-set "{jcl_file}" "{jcl_dataset}({member})"'
    try:
        subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[92m{jcl_file} succesvol geüpload naar {jcl_dataset}({member}).\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mFout bij het uploaden van {jcl_file} naar {jcl_dataset}({member}).\033[0m")
        print(e.stderr)

    # Download het bestand om de inhoud te controleren
    download_file = "downloaded_member.txt"
    download_command = f'zowe zos-files download data-set "{jcl_dataset}({member})" --file "{download_file}"'
    subprocess.run(download_command, shell=True, check=True, capture_output=True, text=True)

    # Controleer of het bestand echt is wat we verwacht hadden
    if os.path.exists(download_file):
        with open(download_file, "r") as f_downloaded:
            downloaded_content = f_downloaded.read().strip()

        if downloaded_content != "":
           print(f"\033[92mHet bestand {jcl_dataset}({member}) is succesvol gevuld.\033[0m")
        else:
             print(f"\033[91mHet bestand {jcl_dataset}({member}) is leeg. QUOTES zullen niet werken.\033[0m")
    else:
        print(f"\033[91mFout bij het downloaden van {jcl_dataset}({member}). Bestand niet gevonden.\033[0m")

    # Verwijder de gedownloade file na controle
    if os.path.exists(download_file):
        os.remove(download_file)

def check_and_create_backup_folder(folder_path):
    """
    Controleer of de backup-folder in de USS bestaat en maak hem aan indien nodig.
    """
    # Zowe CLI commando om te controleren of de folder bestaat
    check_command = f"zowe zos-files list uss-files {folder_path}"
    
    try:
        # Controleer of de folder bestaat
        subprocess.run(check_command, shell=True, capture_output=True, text=True, check=True)
        print(f"\033[92mBackup-folder bestaat al: {folder_path}\033[0m")
    except subprocess.CalledProcessError:
        # Als het folderpad niet bestaat, maak het aan
        print(f"\033[93mBackup-folder bestaat niet. Aanmaken...\033[0m")
        create_command = f"zowe zos-files create uss-directory {folder_path}"
        try:
            subprocess.run(create_command, shell=True, capture_output=True, text=True, check=True)
            print(f"\033[92mBackup-folder succesvol aangemaakt: {folder_path}\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[91mFout bij het aanmaken van de backup-folder:\033[0m {e.stderr}")
        except Exception as e:
            print(f"\033[91mOnverwachte fout opgetreden bij het aanmaken van de backup-folder:\033[0m {str(e)}")

def update_backup_config():
    zos_id = config.zos_id
    folder_name = 'backups'
    
    """
    Update of voeg de USS backup folder toe aan de config file.
    """
    # Prepare de lijn die we willen toevoegen of bijwerken
    folder_line = f"uss_backup_folder = '/z/{zos_id}/{folder_name}'\n"

    # Nieuwe regels voor de config file
    new_lines = []
    folder_exists = False

    # Lees de bestaande config file
    with open(CONFIG_FILE_PATH, 'r') as file:
        lines = file.readlines()

    # Controleer of de 'uss_backup_folder' regel al bestaat
    for line in lines:
        if line.startswith('uss_backup_folder ='):
            new_lines.append(folder_line)  # Update de regel
            folder_exists = True
        else:
            new_lines.append(line)

    # Als de regel niet bestaat, voeg hem toe
    if not folder_exists:
        new_lines.append(folder_line)

    # Schrijf de bijgewerkte regels terug naar de config file
    with open(CONFIG_FILE_PATH, 'w') as file:
        file.writelines(new_lines)

    print(f"Backup folder is ingesteld op: {folder_name}")

    check_and_create_backup_folder(f'/z/{zos_id}/{folder_name}')
