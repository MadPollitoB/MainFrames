# MainFraming: The Game

MainFraming is an interactive game and tool that allows you to manage datasets and files on the mainframe while providing a gamified experience with scores and dynamic quotes. This application leverages Zowe CLI for seamless mainframe interaction and Python for user-friendly operations.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
    - [Menu Options](#menu-options)
3. [Setup Instructions](#setup-instructions)
    - [Requirements](#requirements)
    - [Installation Steps](#installation-steps)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Developer Notes](#developer-notes)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)

---

## Overview

With MainFraming, you can:
- **Create, view, and delete mainframe datasets**.
- **Manage file backups** using USS directories.
- **Track scores**, upload/download scores, and view logs of your actions.
- **Upload and display quotes**, including the "Quote of the Moment."
- **Detect and prevent cheating**, ensuring a fair gaming experience.

---

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

---

## Setup Instructions

### Requirements
1. **Python 3.7+**
2. **Zowe CLI**: Installed and configured for IBM mainframe access.
3. **IBM z/OS ID**: Required for dataset operations.
4. Required Python packages:
   - `pyfiglet` for ASCII art.
   - `requests` for HTTP requests.

### Installation Steps

1. Clone or download this repository to your local machine:
   ```bash
   git clone https://github.com/MadPollitoB/MainFrames.git
   ```
2. Open a terminal in the project directory:
   ```bash
   cd mainframing-game
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r install_files/requirements.txt
   ```
4. Start the program:
   ```bash
   python main.py
   ```

During the first run, you will go through an installation process to set up your z/OS ID, check required datasets, and configure the environment.

---

## Usage

Start the program using `main.py` and follow the menu options. This program is designed for easy interaction with datasets and files on mainframes while adding a gamified scoring element. The intuitive menus make it easy to navigate through the various functionalities.

---

## Configuration

The configuration is stored in `config.py`. This file is automatically updated during the installation. Ensure that Zowe CLI is correctly set up and that you provide the correct z/OS ID.

---

## Developer Notes

1. **Zowe CLI Configuration**:
   Ensure that Zowe CLI is installed and configured correctly. Use `zowe --version` to verify the installation.
2. **Dataset Naming**:
   Use valid dataset naming conventions (e.g., `zXXXXX.DATASET`).

---

## Troubleshooting

- **Zowe CLI Errors**:
  Ensure Zowe CLI is installed and configured with valid credentials.
- **Missing Configurations**:
  Re-run `main.py` to regenerate missing files or configurations.
- **File Upload Errors**:
  Verify that the file path and name are correct.

---

## License

This project is licensed under the `BjornProductions` License.

---

Enjoy exploring the world of IBM mainframes with **MainFraming: The Game**!
