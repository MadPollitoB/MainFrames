import subprocess
import importlib
from install import check_and_create_quotes_dataset, install_dependencies, upload_rexx_script_to_mainframe, upload_jcl_to_mainframe, get_valid_zos_id, update_or_add_zos_id
from menu_functions import main_menu

def main():
    print("De nodige dependencies, datasets en mainframe bestanden worden gecontroleerd en geïnstalleerd!")
    print("Even geduld...")
    print()

    #opvragen IBM login gegevens 
    # Get valid zOS ID from the user
    zos_id = get_valid_zos_id()

    # Update or add the zOS ID in config.py
    update_or_add_zos_id(zos_id)

    # Install dependencies if not already installed
    install_dependencies()
    
    # Create and check if the quotes dataset exists on mainframe
    check_and_create_quotes_dataset()
    
    # Upload the JCL and REXX script to the mainframe
    upload_rexx_script_to_mainframe()  # Upload the REXX script
    upload_jcl_to_mainframe()  # Upload the JCL script

    input("\nPress Enter to start the program.")
   
    main_menu(True)

if __name__ == "__main__":
    main()