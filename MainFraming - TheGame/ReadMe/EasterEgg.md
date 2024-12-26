# Easter Egg Explanation

MainFraming: The Game contains a hidden Easter Egg that activates when specific conditions are met. This feature adds a playful twist to the game and rewards curious users for tampering with the scoring system.

---

## How to Trigger the Easter Egg

The Easter Egg is triggered when **manual changes** are made to the score files (`score.csv` and `logscore.csv`), causing the total scores in these files to no longer match.

### Steps to Trigger:
1. Locate the score files:
   - `score_files/score.csv`
   - `score_files/logscore.csv`
2. Edit these files manually:
   - Open `score.csv` and change the score values in any category.
   - Open `logscore.csv` and change the logged scores in a way that the totals no longer match the values in `score.csv`.
3. Save the changes and run the program (`main.py`).

When the program detects this inconsistency, it assumes tampering has occurred and reveals the Easter Egg.

---

## What Happens During the Easter Egg

When the inconsistency is detected:
1. The screen is cleared.
2. A special title "YOU CHEATER!" is displayed in bold, red text.
3. Messages appear:
   - **Ross from IBM disapproves your actions**: A humorous message highlighting the tampering.
   - **Your scores have been deleted**: The program resets all scores as a penalty.
   - **Björn approves your curiosity**: As a reward, the program grants you 200 bonus points for discovering this hidden feature.
4. Your scores are reset to 0, but the Easter Egg bonus (200 points) is added to the `easteregg` category in the score file.

---

## Technical Details

### Code Logic

- The function `check_cheating` in the `cheating.py` file checks for inconsistencies between `score.csv` and `logscore.csv`.
- It calculates the total scores from both files:
  - `score.csv`: The sum of all category scores.
  - `logscore.csv`: The sum of all logged score entries.
- If these totals do not match, the `handle_cheating` function is called.

### `handle_cheating` Function

This function:
1. Clears the screen using `clear_screen()`.
2. Resets all scores using `reset_scores(message=False)`.
3. Displays the Easter Egg message with ASCII art and colored text.
4. Adds 200 points to the `easteregg` category using `update_score("easteregg", "found", 200)`.

---

## Why an Easter Egg?

The Easter Egg is a fun and interactive way to:
- Reward curious users for exploring and testing the boundaries of the game.
- Add a humorous twist to score tampering.
- Teach users about the consequences of tampering with data in a playful manner.

---

## Disclaimer

The Easter Egg is harmless and designed for entertainment purposes only. However, tampering with the score files will reset all your scores, so proceed with caution if you value your progress in the game.

---

Enjoy exploring the hidden corners of **MainFraming: The Game** and discovering more surprises!