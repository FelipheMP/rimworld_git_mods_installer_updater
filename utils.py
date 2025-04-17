from typing import Union
import os


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


def mod_already_installed(mod_folder_name: str) -> bool:
    """
    Check if a mod is already installed.
    Args:
        mod_folder_name (str): Name of the mod folder.
    Returns:
        bool: True if the mod is already installed, False otherwise.
    """
    return os.path.exists(mod_folder_name)


def check_for_blacklist(blacklist_file_path: str) -> bool:
    """
    Check if the blacklist file exists.
    Args:
        blacklist_file_path (str): Path to the blacklist file.
    Returns:
        bool: True if the blacklist file exists, False otherwise.
    """
    return os.path.exists(blacklist_file_path)


def blacklist_report(blacklist_file_path: str) -> None:
    """
    Check if the blacklist file exists and is not empty.
    If it exists, read the contents and print the blacklisted mods.
    """
    if os.path.exists(blacklist_file_path):
        if is_file_empty(blacklist_file_path):
            print("\nBlacklist file detected but it's empty! No mods will be ignored.")
            return
        with open(blacklist_file_path, "r") as file:
            print("\nBlacklist file detected! Mods below will be ignored:")
            print(file.read().strip())

        if input("\nDo you want to proceed? [y/n]: ").lower() != "y":
            print("Exiting...")
            exit(0)


def is_blacklisted(mod_folder_name: str, blacklist_file_path: str) -> bool:
    """
    Check if a mod is blacklisted.
    Args:
        mod_folder_name (str): Name of the mod folder.
        blacklist_file_path (str): Path to the blacklist file.
    Returns:
        bool: True if the mod is blacklisted, False otherwise.
    """
    if check_for_blacklist(blacklist_file_path):
        with open(blacklist_file_path, "r") as file:
            blacklisted_mods = file.read().splitlines()
            if mod_folder_name in blacklisted_mods:
                print(f"\n{mod_folder_name} is blacklisted. Skipping...")
                return True
    return False
