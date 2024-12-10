# MainFraming - The Game

MainFraming is an interactive game and tool that allows you to manage datasets and files on the mainframe. 
Additionally, you can track scores, upload quotes, and use a dynamic menu.

## Overview
With MainFraming, you can:
- Create, view, and delete mainframe datasets.
- Manage file backups using USS directories.
- Track and upload/download scores.
- Renew and display quotes.

## Installation

### Requirements
1. Python 3.x
2. Zowe CLI configured correctly.
3. Required Python packages installed.
4. required packages (pyfiglet, requests)

### Steps
1. Clone or download this repository to your local machine.
2. Open a terminal in the project directory.
3. Install the required packages:
   ```bash
   pip install -r 
   ```
4. Run the program:
   ```bash
   python main.py
   ```

During the first run, you will go through an installation process to set up your z/OS ID, check required datasets, and configure the environment.

## Features

### Menu Options
#### 1. Manage Datasets
- **View**: Display all datasets on the mainframe.
- **Create**: Add a new dataset.
- **Delete**: Remove an existing dataset.

#### 2. Manage Files
- **View Backup**: Show files in the USS backup directory.
- **Upload**: Send files to the backup directory.
- **Download**: Retrieve files from the backup directory.
- **Delete**: Remove files from the backup directory.

#### 3. View Scores
- Display your current scores.
- View score logs (actions and points).
- Reset scores or upload/download them to/from the mainframe.

#### 4. Manage Quotes
- Display a new "Quote of the Moment."

#### 5. Exit
- Exit the program.

## Configuration
The configuration is stored in `config.py`. This file is automatically updated during the installation. Ensure that Zowe CLI is correctly set up and that you provide the correct z/OS ID.

## Usage
Start the program using `main.py` and follow the menu options. This program is designed for easy interaction with datasets and files on mainframes while adding a gamified scoring element.