import re
import subprocess
from helpers import show_title, clear_screen
from score import update_score
import config

def check_dataset_exists(dataset_name):
    """
    Controleert of een dataset bestaat op het mainframe.
    Retourneert True als de dataset bestaat, anders False.
    """
    check_command = f"zowe zos-files list ds {dataset_name}"
    try:
        result = subprocess.run(check_command, shell=True, check=True, capture_output=True, text=True)
        # Als er geen fout is, betekent dit dat de dataset bestaat
        if result.stdout.strip():  # Als er een output is, betekent dit dat de dataset bestaat
            return True
    except subprocess.CalledProcessError:
        pass  # Geen output betekent de dataset bestaat niet
    return False

def create_dataset(dataset_name, dataset_type="ds"):
    """
    Maakt een dataset aan als deze nog niet bestaat.
    Het type kan "ds" voor een gewone dataset zijn, of "pds" voor een Partitioned Data Set.
    Gebruik "seq" voor sequentiële datasets.
    """
    # Controleer of de dataset bestaat
    if check_dataset_exists(dataset_name):
        print(f"\033[92mDataset {dataset_name} bestaat al.\033[0m")
    else:
        print(f"\033[93mDataset {dataset_name} bestaat niet. Het wordt aangemaakt...\033[0m")
        
        # Voor sequentiële datasets gebruik de juiste optie
        if dataset_type == "seq":
            create_command = f"zowe zos-files create data-set-sequential {dataset_name} --record-format FB --record-length 80 --block-size 800"
        else:
            create_command = f"zowe zos-files create {dataset_type} {dataset_name} --record-format FB --record-length 80 --block-size 800"
        
        try:
            subprocess.run(create_command, shell=True, check=True, capture_output=True, text=True)
            print(f"\033[92mDataset {dataset_name} succesvol aangemaakt.\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[91mFout bij het aanmaken van de dataset {dataset_name}.\033[0m")
            print(e.stderr)

def list_all_datasets(navigate_back, message=""):
    """
    Haalt alle datasets op met behulp van Zowe CLI, gebruikmakend van de zos_id uit config.cfg.
    """
    clear_screen()
    show_title("Zowe Datasets")

    if message != "": 
        print(f"\033[92m{message}\033[0m")
        print()
    else: 
        update_score("datasets", "read", 1)

    # Bouw het Zowe CLI-commando
    list_command = f"zowe zos-files list ds {config.zos_id}.*"

    try:
        # Voer het Zowe CLI-commando uit
        list_ds = subprocess.run(list_command, shell=True, capture_output=True, text=True, check=True)

        # Decodeer en toon de output
        print("Beschikbare DataSets:")
        print("=" * 24)
        print(list_ds.stdout)
    except subprocess.CalledProcessError as e:
        print("\033[91m\nFout bij ophalen van datasets:\033[0m")
        print(e.stderr)
    except FileNotFoundError:
        print("\033[91m\nZowe CLI niet gevonden. Zorg ervoor dat Zowe CLI is geïnstalleerd en geconfigureerd.\033[0m")

    input("\nDruk op Enter om terug te gaan.")

    # Gebruik de callback om terug te navigeren
    navigate_back()

def create_new_dataset(navigate_back):
    """
    Creëert een dataset met Zowe CLI, gebruikmakend van de zos_id uit config.cfg.
    Geeft succes- of foutmeldingen weer.
    """
    clear_screen()
    show_title("Zowe Datasets")

    # Vraag de gebruiker om een datasetnaam
    datasetnaam = ""
    while not datasetnaam: 
        datasetnaam = input("Voer een naam in voor de nieuwe dataset: ").strip()

        if not datasetnaam:
            print("\033[91m\nGeen datasetnaam opgegeven. Probeer opnieuw.\033[0m")
        
        if not re.match("^[a-zA-Z0-9]+$", datasetnaam):
           print("\033[91m\nOngeldige naam. Gebruik alleen letters en cijfers.\033[0m")
           datasetnaam = ""
    
    datasetnaam = datasetnaam.lower()

    # Bouw de volledige naam van de dataset
    dataset_name = f"{config.zos_id}.{datasetnaam}"

    # Maak de dataset aan (gebruik de create_dataset functie)
    create_dataset(dataset_name, dataset_type="ds")

    # Na het succesvol aanmaken van de dataset, toon de datasets
    update_score("datasets", "create", 5)
    list_all_datasets(navigate_back, "Dataset succesvol aangemaakt!")

def delete_dataset(navigate_back):
    """
    Verwijdert een dataset met behulp van Zowe CLI.
    Toont eerst een genummerde lijst van datasets, waarna de gebruiker een keuze maakt.
    """
    clear_screen()

    show_title("Zowe Datasets")

    # Stap 1: Haal alle beschikbare datasets op
    list_command = f"zowe zos-files list ds {config.zos_id}.*"
    try:
        result = subprocess.run(list_command, shell=True, capture_output=True, text=True, check=True)
        datasets = result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        print("\033[91m\nFout bij ophalen van datasets:\033[0m")
        print(e.stderr)
        input("\nDruk op Enter om terug te gaan.")
        navigate_back()
        return

    # Controleer of er datasets zijn
    if not datasets:
        print("\033[93m\nGeen datasets gevonden om te verwijderen.\033[0m")
        input("\nDruk op Enter om terug te gaan.")
        navigate_back()
        return

    # Stap 2: Toon een genummerde lijst van datasets
    print("Beschikbare DataSets:")
    for i, dataset in enumerate(datasets, start=1):
        print(f"{i}. {dataset}")

    print("q. back to dataset menu")
    
    # Stap 3: Vraag de gebruiker om een keuze
    while True:
        choice = input("\nVoer het nummer in van de dataset die je wilt verwijderen of 'q' om terug te gaan: ").strip().lower()

        if choice == 'q':
            # Als de gebruiker 'q' invoert, ga terug naar het datasetmenu
            navigate_back()
            return

        try:
            # Probeer de keuze te converteren naar een integer
            choice = int(choice)
            if choice < 1 or choice > len(datasets):
                print("\033[91m\nError: Verkeerde invoer! Kies een geldig nummer of 'q' om terug te gaan.\033[0m")
            else:
                break  # Breek uit de loop als de invoer geldig is
        except ValueError:
            # Als de invoer geen geldig nummer is, toon een foutmelding
            print("\033[91m\nError: Verkeerde invoer! Kies een geldig nummer of 'q' om terug te gaan.\033[0m")

    # Stap 4: Verwijder de gekozen dataset
    dataset_to_delete = datasets[choice - 1]
    delete_command = f"zowe zos-files delete data-set {dataset_to_delete} -f"
    try:
        subprocess.run(delete_command, shell=True, check=True, capture_output=True, text=True)
        update_score("datasets", "delete", 5) 
        list_all_datasets(navigate_back, "Dataset succesvol verwijderd!")

    except subprocess.CalledProcessError as e:
        clear_screen()
        print("\033[91mDataset verwijderen is niet gelukt.\033[0m")
        print(f"\nDetails van de fout:\n{e.stderr}")
        input("Druk op Enter om door te gaan.")
        navigate_back()
