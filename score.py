import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORE_FILES_DIR = os.path.join(BASE_DIR, "score_files")

# Functie om de score op te slaan in score.csv
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
            writer.writerow(["category", "score"])  # Header toevoegen
            writer.writerow([category, added_score])

    # Log the score change
    log_score_change(category, action, added_score)

# Functie om logscore.csv bij te werken met tijdstempel
def log_score_change(category, action, added_score):
    log_file = os.path.join(SCORE_FILES_DIR, "logscore.csv")
    current_time = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    new_row = [current_time, category, action, added_score]

    try:
        # Lees de bestaande inhoud van logscore.csv
        with open(log_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Voeg de nieuwe regel bovenaan de lijst
        rows.insert(0, new_row)

        # Schrijf de bijgewerkte inhoud terug naar het bestand
        with open(log_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    except FileNotFoundError:
        # Als het bestand niet bestaat, maak het dan aan en voeg de eerste regel toe
        with open(log_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["datetime", "category", "action", "added_score"])  # Header toevoegen
            writer.writerow(new_row)  # Voeg de eerste logregel toe

# Functie om de huidige score te tonen
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

# Functie om de score logging te tonen
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

# Functie om scores te resetten
def reset_scores():
    score_file = os.path.join(SCORE_FILES_DIR, "score.csv")
    log_file = os.path.join(SCORE_FILES_DIR, "logscore.csv")
    
    while True:
        confirm = input("Ben je zeker dat je de score wilt resetten? Dit zal de scorebestanden verwijderen. (y/n): ").strip().lower()

        if confirm == 'y':
            # Verwijder de bestaande bestanden
            if os.path.exists(score_file):
                os.remove(score_file)
                print("\033[92mscore.csv bestand is verwijderd.\033[0m")
            
            if os.path.exists(log_file):
                os.remove(log_file)
                print("\033[92mlogscore.csv bestand is verwijderd.\033[0m")

            # Maak de bestanden opnieuw aan met de juiste headers
            with open(score_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["category", "score"])  # Header toevoegen
            print("\033[92mscore.csv bestand opnieuw aangemaakt.\033[0m")

            with open(log_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["datetime", "category", "action", "added_score"])  # Header toevoegen
            print("\033[92mlogscore.csv bestand opnieuw aangemaakt.\033[0m")

            break

        elif confirm == 'n':
            print("\033[93mResetten van de score is geannuleerd.\033[0m")
            break

        else:
            print("\033[91mOngeldige keuze. Voer 'y' in om de score te resetten of 'n' om de actie te annuleren.\033[0m")
