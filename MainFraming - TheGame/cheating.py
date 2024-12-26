import os
from score import reset_scores, update_score
from helpers import clear_screen, show_title

def check_cheating(score_file, log_file):
    total_score = 0
    log_total = 0

    # Check if score file exists and process its data
    if os.path.exists(score_file):
        with open(score_file, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:  # Skip header row
                # print(f"Processing line in score file: {line.strip()}")  # Debug print
                parts = line.strip().split(',')
                if len(parts) == 2:  # Validate row format
                    try:
                        total_score += int(parts[1])  # Accumulate score
                    except ValueError as e:
                        # print(f"Invalid score in line: {line.strip()} - Error: {e}")
                        continue  # Skip invalid rows

    # Check if log file exists and process its data
    if os.path.exists(log_file):
        with open(log_file, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:  # Skip header row
                # print(f"Processing line in log file: {line.strip()}")  # Debug print
                parts = line.strip().split(',')
                if len(parts) == 4:  # Validate row format
                    try:
                        log_total += int(parts[3])  # Accumulate log score
                    except ValueError as e:
                        # print(f"Invalid log score in line: {line.strip()} - Error: {e}")
                        continue  # Skip invalid rows

    # Check if totals are inconsistent
    if total_score != log_total:
        handle_cheating()

def handle_cheating():
    clear_screen()
    reset_scores(message=False)

    show_title('YOU CHEATER!', additional=False)
    print("\033[91mRoss From IBM Disapproved This Action\033[0m")
    print("\033[93mYour scores have been deleted.\033[0m")
    print("\033[94mYou gain 200 points for finding this EasterEgg because Björn Approves This Action\033[0m")
    
        # ASCII art of an Easter egg
    easter_egg_art = """
              ,,..,,,,..,,,.., 
          .,%%%%%;;%%%;;%%%%;;%%,. 
       .;;%%%"""""''""''"""''";%%%;;, 
     .;%%%%'                    `;;%%%, 
   .%%%%;'                        `%%%;; 
  .%%%;;'      .sSSSSs.            `%%;;, 
  %%;;%'      .SSSSSSSS,%%%%,      `%;;%% 
 .;;%%% .::::.SSSSSSSSSS,%%%%%,oOOOo;;%%%, 
 %%%%;'.:xXXXXx!SSSSSSS!a@@@@@a!OOOOO%%%;; 
 %%;;% :XXXXXXXX!SSSSS!@@@@@@@@@!OOOO%%;;% 
 ;;%%% XXXXXXXXXX!SSS!@@@@@@@@@@@!OOO;;%%% 
a@@a@@a@@a@@a@@a@@a@@a@@a@@a@@a@.sSSSSSs.sSSs.sSSSSs. 
`;%%%;|;%%%;|;%%%;|;%%%;|;%%%;|,SSssssSS;SSSS;SSsssSS 
.%;|;%%%;|;%%%;|;%%%;|;%%%;|;%%,SSSSSSSS;SSSS;SSSSSSS 
`;%%%;|;%%%;|;%%%;|;%%%;|;%%%;|;`SSSSSS'^ssss^`SSSSS' 
.%;|;%%%;|;%%%;|;%%%;|;%%%;|;%%%;|;%,ssSSS'`SSSsss, 
`;%%%;|;%%%;|;%%%;|;%%%;|;%%%;|;%%%,SSSSSS' `SSSSSS 
 .;|;%%%;|;%%%;|;%%%;|;%%%;|;%%%;|,SSSSSS'  ,SSSSSS 
 `%%%;|;%%%;|;%%%;|;%%%;|;%%%;|;,SSS^SS'%  ,SSSSSS' 
  `|;%%%;|;%%%;|;%%%;|;%%%;|;%%,S';%%`S'  ,SSS^SSS 
    `;|;%%%;|;%%%;|;%%%;|;%%%;|;%%%;|;'   `S'  `S' 
    """
    print("\033[95m" + easter_egg_art + "\033[0m")  # Use green text for the art

    # Bonus Easter Egg Score
    update_score("easteregg", "found", 200)

    # start the game
    input("\nPress Enter to start the program.")