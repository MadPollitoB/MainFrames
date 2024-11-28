import subprocess
import os
import sys
from helpers import show_title, clear_screen,start_job_randomquote
from datasets_functions import list_all_datasets, create_dataset, delete_dataset, create_new_dataset, download_scores, upload_scores, list_numeric_datasets
from score import show_score, show_score_logging, reset_scores
import config


def delete_local_file(local_file):
    """
    Verwijdert het opgegeven bestand als het bestaat.
    """
    os.remove(local_file)

def get_quote_of_the_moment():
    """
    Haalt de quote van het moment op uit de dataset, retourneert deze, 
    en verwijdert het bestand na gebruik.
    """
    # Zet het vaste z/OS datasetnaam in
    dataset_name = f"{config.zos_id}.QUOTES.MOMENT"
    local_file = "downloaded_quotes_moment.txt"

    # Zowe CLI om de quote van het moment op te halen door de dataset te downloaden
    command = f"zowe zos-files download data-set '{dataset_name}' --file {local_file}"

    try:
        # Voer het downloadcommando uit
        subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        # print(f"\033[92mDataset {dataset_name} succesvol gedownload naar {local_file}.\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mFout bij het downloaden van dataset {dataset_name}.\033[0m")
        print(e.stderr)
        # Verwijder bestand als het is aangemaakt tijdens een foutieve poging
        delete_local_file(local_file)
        return "Geen quote beschikbaar."

    # Lees de inhoud van het gedownloade bestand
    lines = []  # Initieer 'lines' als een lege lijst
    if os.path.exists(local_file):
        with open(local_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

    # Verwijder het bestand nadat het is gelezen of een fout is opgetreden
    delete_local_file(local_file)

    # Controleer of er regels in het bestand zijn en retourneer de eerste regel als de quote
    if len(lines) > 0:
        quote_of_the_moment = lines[0].strip()
    else:
        quote_of_the_moment = "Geen quote beschikbaar."

    return quote_of_the_moment

def main_menu(quoterandomise=False):
    """Toont het hoofdmenu."""
    clear_screen()
    show_title('MainFraming', 'The Game')
    
    print("ophalen quote:...")
  
    if quoterandomise:
        start_job_randomquote()


    # Haal de quote van het moment op
    quote = get_quote_of_the_moment()
    

    sys.stdout.write("\033[F")  # Verplaatst de cursor één regel omhoog
    sys.stdout.write("\033[K")  # Wis de hele regel
    sys.stdout.flush()
    
    print("*" * 64)
    print(f"* {quote.center(60)} *")
    print("*" * 64) 
    print() 

    # print main menu
    print("Main Menu")
    print("=" * 9)
    print("1. DataSets")
    print("2. Dataset Inhoud")
    print("3. Score")
    print("4. Change Quote")
    print("5. Afsluiten")

    keuze = input("Maak een keuze: ")
    if keuze == '1':
        datasets_menu()
    elif keuze == '2':
        dataset_members_menu()
    elif keuze == '3':
        score_menu()
    elif keuze == '3':
        main_menu(True)
    elif keuze == '4':
        exit_app()
    else:
        print("\033[91m\nOngeldige keuze. Probeer opnieuw.\033[0m")
        input("Druk op Enter om verder te gaan...")
        main_menu()

def dataset_members_menu(dataset_mod=""):
    """Toont het DataSets-menu."""
    clear_screen()
    show_title('DataSets')

    if ({dataset_mod}==""):
        list_numeric_datasets()
        dataset_mod = input("Kies de dataset die je wil modificeren: ")
        dataset_members_menu(dataset_mod)

    print()
    print(f"Gekozen dataset: {dataset_mod}")
    print()
    print("Kies uit volgende opties:")
    print("=" * 24)
    print("1. Geef de inhoud van de dataset")
    print("2. Pas de Dataset aan")
    print("3. Vewijder de inhoud van de datset")
    print("4. Kies een nieuwe dataset")
    print("5. Terug naar hoofdmenu")
    print("6. Aflsuiten")

    keuze = input("Maak een keuze: ")
    if keuze == '1':
        print("toon inhoud") 
    elif keuze == '2':
        print("modify inhoud") 
    elif keuze == '3':
        print("verwijder inhoud") 
    elif keuze == '4':
        list_numeric_datasets()
        dataset_mod = input("Kies de dataset die je wil modificeren: ")
        dataset_members_menu(dataset_mod)
    elif keuze == '6':
        main_menu()
    elif keuze == '7':
        exit_app()
    else:
        print("\033[91m\nOngeldige keuze. Probeer opnieuw.\033[0m")
        input("Druk op Enter om verder te gaan...")
        dataset_members_menu(dataset_mod)

def datasets_menu():
    """Toont het DataSets-menu."""
    clear_screen()
    show_title('DataSets')
    
    print("=" * 24)
    print("1. Toon alle Datasets")
    print("2. Dataset Aanmaken")
    print("3. Dataset Verwijderen")
    print("4. Terug naar hoofdmenu")
    print("5. Aflsuiten")

    keuze = input("Maak een keuze: ")
    if keuze == '1':
        list_all_datasets(navigate_back=datasets_menu) 
    elif keuze == '2':
        create_new_dataset(navigate_back=datasets_menu)
    elif keuze == '3':
        delete_dataset(navigate_back=datasets_menu)
    elif keuze == '4':
        main_menu()
    elif keuze == '5':
        exit_app()
    else:
        print("\033[91m\nOngeldige keuze. Probeer opnieuw.\033[0m")
        input("Druk op Enter om verder te gaan...")
        datasets_menu()

def score_menu():
    """Toont het Score-menu."""
    clear_screen()
    show_title('Score Menu')
    print("Kies uit volgende opties:")
    print("=" * 24)
    print("1. Toon score")
    print("2. Toon score logging")
    print("3. reset scores")
    print("4. download scores from mainframe")
    print("5. upload scores to mainframe")
    print("6. Terug naar hoofdmenu")
    print("7. Afsluiten")

    keuze = input("Maak een keuze: ")
    if keuze == '1':
        print()
        show_score()  # Show current score
        input("\nDruk op Enter om verder te gaan...")
        score_menu()
    elif keuze == '2':
        print()
        show_score_logging()  # Show score log
        input("\nDruk op Enter om verder te gaan...")
        score_menu()
    elif keuze == '3':
        print()
        reset_scores()
        input("\nDruk op Enter om verder te gaan...")
        score_menu()
    elif keuze == '4':
        print()
        download_scores()
        input("\nDruk op Enter om verder te gaan...")
        score_menu()
    elif keuze == '5':
        print()
        upload_scores()
        input("\nDruk op Enter om verder te gaan...")
        score_menu()
    elif keuze == '6':
        main_menu()
    elif keuze == '7':
        exit_app()
    else:
        print("\033[91m\nOngeldige keuze. Probeer opnieuw.\033[0m")
        input("Druk op Enter om verder te gaan...")
        score_menu()

def exit_app():
    """Sluit de applicatie af."""
    print("\033[93mApplicatie wordt afgesloten.\033[0m")
    exit()
