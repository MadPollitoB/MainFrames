import re
import os
import subprocess
from score import update_score
import config
from helpers import show_title, clear_screen
from score import update_score
import config

def list_all_uss_files(navigate_back, message=""):
    """
    Haalt alle bestanden op in de backup-folder van de USS met behulp van Zowe CLI, 
    gebruikmakend van de USS pad uit config.cfg.
    
    Score wordt alleen bijgewerkt als het ophalen van de bestanden succesvol was.
    """
    clear_screen()
    show_title("USS Backup Files")

    if message != "":
        print(f"\033[92m{message}\033[0m\n")

    uss_backup_folder = config.uss_backup_folder

    # Bouw het Zowe CLI-commando
    list_command = f"zowe zos-files list uss-files {uss_backup_folder}"

    try:
        # Voer het Zowe CLI-commando uit
        list_files = subprocess.run(list_command, shell=True, capture_output=True, text=True, check=True)

        # Decodeer de output
        files = list_files.stdout.splitlines()  # Splits de output in individuele regels

        # Gebruik regex om hele bestandsnamen te extraheren, inclusief spaties
        files_and_types = []
        for line in files:
            # Regex om naam en type te scheiden
            match = re.match(r'^(.+?)\s+(-[rwx-]+)\s+', line)
            if match:
                files_and_types.append(f"{match.group(1)}")

        # Toon de bestanden
        print("Beschikbare bestanden in de USS-backupfolder:")
        print("=" * 45)
        if files_and_types:
            for file in files_and_types:
                print(file)
        else:
            print("\033[93mGeen bestanden gevonden in de backup-folder.\033[0m")

        # Score wordt alleen bijgewerkt als we de bestanden succesvol konden ophalen
        update_score("files", "list", 1)

    except subprocess.CalledProcessError as e:
        print("\033[91m\nFout bij ophalen van bestanden uit USS:\033[0m")
        print(e.stderr)
    except Exception as e:
        print("\033[91m\nOnverwachte fout opgetreden:\033[0m")
        print(str(e))

    input("\nDruk op Enter om terug te gaan.")

    # Gebruik de callback om terug te navigeren
    navigate_back()

def upload_files_to_backup(navigate_back):
    """
    Upload bestanden naar de USS-backupfolder met behulp van Zowe CLI.
    Voeg 5 punten toe bij succesvolle uploads en toon een succesbericht.
    """
    clear_screen()
    show_title("Upload Bestanden naar USS Backup")

    while True:
        # Vraag om een bestandsnaam
        bestandspad = input("Voer het volledige pad in van het bestand dat je wilt uploaden (of 'q' om terug te gaan): ").strip()

        # Controleer of de gebruiker terug wil naar het menu
        if bestandspad.lower() == 'q':
            print("Terug naar het menu...")
            navigate_back()
            return

        # Controleer of het bestand bestaat
        if not os.path.isfile(bestandspad):
            print("\033[91m\nHet opgegeven bestand bestaat niet. Probeer opnieuw.\033[0m")
            continue

        # Controleer op een geldige bestandsnaam
        bestandsnaam = os.path.basename(bestandspad)
        if not re.match(r"^[a-zA-Z0-9_.\-\s]+$", bestandsnaam):
            print("\033[91m\nOngeldige bestandsnaam. Gebruik alleen letters, cijfers, spaties, underscores, of streepjes.\033[0m")
            continue

        # Bouw het Zowe CLI-commando voor upload
        uss_backup_folder = config.uss_backup_folder
        doelpad = f"{uss_backup_folder}/{bestandsnaam}"
        upload_command = f'zowe zos-files upload file-to-uss "{bestandspad}" "{doelpad}" --binary'

        try:
            # Voer het uploadcommando uit
            subprocess.run(upload_command, shell=True, check=True, capture_output=True, text=True)
            print(f"\033[92m Bestand succesvol geüpload: {bestandspad} naar {doelpad}\033[0m")

            # Voeg punten toe en toon succesbericht
            update_score("files", "upload", 5)
            print("5 punten toegevoegd voor de upload.\n")

        except subprocess.CalledProcessError as e:
            print(f"\033[91m Fout bij uploaden van bestand: {e.stderr}\033[0m")
            continue

        # Vraag of de gebruiker nog een bestand wil uploaden
        doorgaan = input("Wil je nog een bestand uploaden? (y/n): ").strip().lower()
        if doorgaan != 'y':
            print("Terug naar het menu...")
            navigate_back()
            return