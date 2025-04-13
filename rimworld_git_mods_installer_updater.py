from typing import Union
import sys
import os
import json
import subprocess
import shutil
import time
import mods_list
import mods_list_formater

with open("config.json", "r") as config_file:
    config = json.load(config_file)

BLACKLIST_CONFIG_FILE = config["blacklist_file"]
MODS_PY_PATH = config["mods_py_path"]
MODS_TXT_PATH = config["mods_txt_path"]
UPDATE_LOG_PATH = config["update_log_path"]


CHECK_UPDATES_ONLY = False
is_check_updates_only = CHECK_UPDATES_ONLY
COMPLETION_MESSAGE = "Done!"


# Utility Functions
def is_file_empty(file_path: Union[str, os.PathLike[str]]) -> bool:
    """
    Check if a file is empty.

    Args:
        file_path (str): Path to the file.

    Returns:
        bool: True if the file is empty, False otherwise.
    """
    try:
        return os.stat(file_path).st_size == 0
    except FileNotFoundError:
        print(f"\nFile {file_path} not found.")
        return True
    except PermissionError:
        print(f"\nPermission denied to access {file_path}.")
        return True
    except Exception as e:
        print(f"\nAn error occurred while checking {file_path}: {e}")
        return True


def check_for_blacklist():
    return os.path.exists(BLACKLIST_CONFIG_FILE)


def blacklist_report():
    """
    Check if the blacklist file exists and is not empty.

    If it exists, read the contents and print the blacklisted mods.
    """
    if os.path.exists(BLACKLIST_CONFIG_FILE):
        if is_file_empty(BLACKLIST_CONFIG_FILE):
            print("\nBlacklist file detected but it's empty! No mods will be ignored.")
            return
        with open(BLACKLIST_CONFIG_FILE, "r") as file:
            print("\nBlacklist file detected! Mods below will be ignored:")
            print(file.read().strip())

        if input("\nDo you want to proceed? [y/n]: ").lower() != "y":
            print("Exiting...")
            exit(0)


def is_blacklisted(mod_folder_name: str) -> bool:
    """
    Check if a mod is blacklisted.

    Args:
        mod_folder_name (str): Name of the mod folder.

    Returns:
        bool: True if the mod is blacklisted, False otherwise.
    """
    if check_for_blacklist():
        with open(BLACKLIST_CONFIG_FILE, "r") as file:
            blacklisted_mods = file.read().splitlines()
            if mod_folder_name in blacklisted_mods:
                print(f"\n{mod_folder_name} is blacklisted. Skipping...")
                return True
    return False


def mod_already_installed(mod_folder_name: str) -> bool:
    """
    Check if a mod is already installed.

    Args:
        mod_folder_name (str): Name of the mod folder.

    Returns:
        bool: True if the mod is already installed, False otherwise.
    """
    return os.path.exists(mod_folder_name)


# Mods List Management
def verify_mods_folder():
    """Verify if the script is running in the correct directory."""
    curr_dir_name = os.path.basename(os.getcwd())
    if curr_dir_name != "Mods":
        print("\nPlace the scripts in your RimWorld/Mods/ folder before running it!")
        input("\nPress Enter to exit...")
        exit(0)


def verify_mods_list():
    """Verify the mods list files and update them if necessary."""
    try:
        if os.path.exists(MODS_TXT_PATH):
            mods_txt_mod_time = os.path.getmtime(MODS_TXT_PATH)

            if os.path.exists(MODS_PY_PATH):
                mods_py_mod_time = os.path.getmtime(MODS_PY_PATH)

                with open(MODS_PY_PATH, "r") as file:
                    mods_py_content = file.read()

                if (
                    is_file_empty(MODS_PY_PATH)
                    or (mods_txt_mod_time > mods_py_mod_time)
                    or "mods: List[Tuple[str, str]] = []" in mods_py_content
                ):
                    print(f"\n{MODS_TXT_PATH} file identified!")
                    print(f"Sorting mods in {MODS_TXT_PATH} file alphabetically...")
                    mods_list_formater.sorting_modslist_txt(MODS_TXT_PATH)
                    print(f"Updating {MODS_PY_PATH} file...")
                    mods_list_formater.process_file(MODS_TXT_PATH, MODS_PY_PATH)
                    print(COMPLETION_MESSAGE)
                    exit(0)

        else:
            print(f"\n{MODS_TXT_PATH} file not found. Creating new example file...")
            with open(MODS_TXT_PATH, "w") as file:
                file.write(
                    "PerformanceOptimizer https://github.com/Taranchuk/PerformanceOptimizer.git\n"
                )
                file.write(
                    "JustPutItOverThere https://github.com/emipa606/JustPutItOverThere.git\n"
                )
                file.write(
                    "OwlAnimalGear https://github.com/Owlchemist/animal-gear.git\n"
                )
            print(f"{MODS_TXT_PATH} file created!")
            print(f"Sorting mods in {MODS_TXT_PATH} file alphabetically...")
            print(COMPLETION_MESSAGE)
            mods_list_formater.sorting_modslist_txt(MODS_TXT_PATH)
            print(
                "\nAdd mods by typing its name followed by its git repo url as is shown in the example file!"
            )
            print("To remove it, well, delete its name and url line.")
            print(
                "\nTip: You can create a file named blacklist.conf and add mod folder names in it."
            )
            print("Add each mod folder name in a new line.")
            print("Matching mod folder names will be ignored by the updater/installer!")
            print(f"\nUpdating {MODS_PY_PATH} file...")
            mods_list_formater.process_file(MODS_TXT_PATH, MODS_PY_PATH)
            print(COMPLETION_MESSAGE)
            print("\nRun this script again to install/update the mods in the list.")
            exit(0)
    except (FileNotFoundError, PermissionError) as e:
        print(f"\nError accessing mods list files: {e}")
    except Exception as e:
        print(f"\nUnexpected error verifying mods lists: {e}")


# User Interactions
def ask_update_mode():
    """
    Ask the user if they want to check for updates only.

    Returns:
        bool: True if the user wants to check for updates only, False otherwise.
    """
    try:
        input_str = (
            input("\nDo you want to check for updates only? [y/n]: ").strip().lower()
        )
        print()
        if input_str in ["y", "n"]:
            return input_str == "y"
    except Exception as e:
        print(f"\nError reading input: {e}")


def ask_install_mod(mod_folder_name: str, git_url: str):
    """
    Ask the user if they want to install a mod.

    Args:
        mod_folder_name (str): Name of the mod folder.
        git_url (str): Git URL of the mod repository.
    """
    try:
        input_str = (
            input(
                f"\n/Mods/{mod_folder_name}/ folder not found. Would you like to install it? [y/n]: "
            )
            .strip()
            .lower()
        )
        if input_str.lower() == "y":
            git_install(git_url)
        else:
            print(f"Skipping {mod_folder_name} installation.")
            return
    except Exception as e:
        print(f"\nError reading input: {e}")


# Git Operations
def git_update(mod_folder_name: str, git_url: str):
    """
    Update a mod using git.

    Args:
        mod_folder_name (str): Name of the mod folder.
        git_url (str): Git URL of the mod repository.
    """
    if is_blacklisted(mod_folder_name):
        return

    if mod_already_installed(mod_folder_name):
        if not is_check_updates_only:
            print(f"\n{mod_folder_name} is already installed. Skipping...")
        return

    update_repo(mod_folder_name, git_url)


def update_repo(mod_folder_name: str, git_url: str):
    """
    Update the mod repository.

    Args:
        mod_folder_name (str): Name of the mod folder.
        git_url (str): Git URL of the mod repository.
    """
    if os.path.exists(mod_folder_name):
        print(f"Updating {mod_folder_name}...")
        os.chdir(mod_folder_name)
        try:
            if os.path.exists(".git"):
                subprocess.run(["git", "fetch"])
                result = subprocess.run(["git", "pull"], capture_output=True, text=True)
                if "Already up to date." not in result.stdout:
                    os.chdir("..")
                    log_update(mod_folder_name)
                else:
                    print("Already up to date!")
                    os.chdir("..")
            else:
                handle_missing_git_folder(mod_folder_name, git_url)
        except subprocess.CalledProcessError as e:
            print(f"\nError updating {mod_folder_name}: {e}")
        finally:
            os.chdir("..")
    else:
        if not is_check_updates_only:
            ask_install_mod(mod_folder_name, git_url)


def git_install(git_url: str):
    """
    Clone a git repository.

    Args:
        git_url (str): Git URL of the mod repository.
    """
    try:
        subprocess.run(["git", "clone", git_url])
    except subprocess.CalledProcessError as e:
        print(f"\nError cloning repository {git_url}: {e}")


def git_remove_install(mod_folder_name: str, git_url: str):
    """
    Remove and reinstall a git repository.

    Args:
        mod_folder_name (str): Name of the mod folder.
        git_url (str): Git URL of the mod repository.
    """
    input_str = input(
        f"\nDeleting and reinstalling mod /{mod_folder_name}/... Are you sure? [IAMSURE/n]: "
    )
    if input_str.lower() == "iamsure":
        shutil.rmtree(mod_folder_name)
        git_install(git_url)


def handle_missing_git_folder(mod_folder_name: str, git_url: str):
    """
    Handle the case where the .git folder is missing.

    Args:
        mod_folder_name (str): Name of the mod folder.
        git_url (str): Git URL of the mod repository.
    """
    os.chdir("..")
    if not is_check_updates_only:
        print(f"\n.git not found in /{mod_folder_name}/.")
        input_str = input(
            "Would you like to DELETE /{mod_folder_name}/ and reinstall correctly for auto-update? [IAMSURE/n]: "
        )
        if input_str.lower() == "iamsure":
            git_remove_install(mod_folder_name, git_url)


# Logging
def log_update(mod_folder_name: str):
    """
    Log the update of a mod.

    Args:
        mod_folder_name (str): Name of the mod folder.
    """
    try:
        print(f"Attempting to log update for {mod_folder_name}")
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        latest_commit_date, latest_commit_hour = "Unknown", "Unknown"

        # Fetch the timestamp of the last commit
        try:
            latest_git_commit_timestamp = subprocess.check_output(
                ["git", "show", "--format=%ci", "HEAD"],
                cwd=mod_folder_name,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
            if latest_git_commit_timestamp:
                latest_commit_date = latest_git_commit_timestamp.split(" ")[
                    0
                ]  # Extract the date part
                latest_commit_hour = latest_git_commit_timestamp.split(" ")[
                    1
                ]  # Extract the date part
        except subprocess.CalledProcessError as e:
            print(
                f"\nError fetching latest commit timestamp for {mod_folder_name}: {e}"
            )
            latest_commit_date, latest_commit_hour = "Unknown", "Unknown"

        try:
            if os.path.exists(UPDATE_LOG_PATH):
                with open(UPDATE_LOG_PATH, "a") as log_file:
                    log_file.write(
                        f"\n{mod_folder_name} was updated on {current_time}\n"
                    )
                    log_file.write(
                        f"Latest commit date and hour: {latest_commit_date} {latest_commit_hour}\n"
                    )
                    log_file.write(
                        "------------------------------------------------------------------\n"
                    )
            else:
                with open(UPDATE_LOG_PATH, "w") as log_file:
                    log_file.write("Update History:\n")
                    log_file.write(
                        "##################################################################\n"
                    )
                    log_file.write(
                        f"\n{mod_folder_name} was updated on {current_time}\n"
                    )
                    log_file.write(
                        f"Latest commit date and hour: {latest_commit_date} {latest_commit_hour}\n"
                    )
                    log_file.write(
                        "------------------------------------------------------------------\n"
                    )
            print(f"Update for {mod_folder_name} logged successfully.")
        except (FileNotFoundError, PermissionError) as e:
            print(f"\nError writing to log file: {e}")
    except Exception as e:
        print(f"\nUnexpected error logging update for {mod_folder_name}: {e}")


# Main Script Execution
if __name__ == "__main__":
    verify_mods_folder()
    verify_mods_list()
    check_for_blacklist()
    blacklist_report()

    # Default values
    start_index = 0
    count = len(mods_list.mods)

    # Check if command-line arguments are provided
    if len(sys.argv) > 1:
        try:
            start_index = int(sys.argv[1])
            count = int(sys.argv[2])
            is_check_updates_only = True
        except ValueError:
            print("\nInvalid arguments. Using defaults.")
    else:
        if not is_check_updates_only:
            is_check_updates_only = ask_update_mode()

    # Calculate end index
    end_index = min(start_index + count, len(mods_list.mods))

    # Slicing the mods list
    mods_to_update = mods_list.mods[start_index:end_index]

    for mod_folder_name, git_url in mods_to_update:
        git_update(mod_folder_name, git_url)

    print(f"\n{COMPLETION_MESSAGE}")

    print("\nMade with <3 by @FelipheMP")
    input("Press Enter to exit...")
