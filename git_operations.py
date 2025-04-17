import os
import subprocess
import shutil
import logs
import user_interactions
import utils


def git_update(
    mod_folder_name: str,
    git_url: str,
    blacklist_file_path: str,
    is_check_updates_only: bool,
):
    """
    Update a mod using git.
    Args:
        mod_folder_name (str): Name of the mod folder.
        git_url (str): Git URL of the mod repository.
        blacklist_file_path (str): Path to the blacklist file.
        is_check_updates_only (bool): Flag to indicate if only updates are checked.
    """
    if utils.is_blacklisted(mod_folder_name, blacklist_file_path):
        return

    if utils.mod_already_installed(mod_folder_name):
        if is_check_updates_only:
            update_repo(
                mod_folder_name, git_url, blacklist_file_path, is_check_updates_only
            )
        else:
            print(f"\n{mod_folder_name} is already installed. Skipping...")


def update_repo(
    mod_folder_name: str,
    git_url: str,
    update_log_path: str,
    is_check_updates_only: bool,
):
    """
    Update the mod repository.
    Args:
        mod_folder_name (str): Name of the mod folder.
        git_url (str): Git URL of the mod repository.
    """
    if os.path.exists(mod_folder_name):
        print(f"\nUpdating {mod_folder_name}...")
        os.chdir(mod_folder_name)
        try:
            if os.path.exists(".git"):
                subprocess.run(["git", "fetch"])
                result = subprocess.run(["git", "pull"], capture_output=True, text=True)
                if "Already up to date." not in result.stdout:
                    os.chdir("..")
                    logs.log_update(mod_folder_name, update_log_path)
                else:
                    print("Already up to date!")
                    os.chdir("..")
            else:
                handle_missing_git_folder(
                    mod_folder_name, git_url, is_check_updates_only
                )
        except subprocess.CalledProcessError as e:
            print(f"\nError updating {mod_folder_name}: {e}")
    else:
        if not is_check_updates_only:
            user_interactions.ask_install_mod(mod_folder_name, git_url)


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


def handle_missing_git_folder(
    mod_folder_name: str, git_url: str, is_check_updates_only: bool
):
    """
    Handle the case where the .git folder is missing.
    Args:
        mod_folder_name (str): Name of the mod folder.
        git_url (str): Git URL of the mod repository.
        is_check_updates_only (bool): Flag to indicate if only updates are checked.
    """
    os.chdir("..")
    if not is_check_updates_only:
        print(f"\n.git not found in /{mod_folder_name}/.")
        input_str = input(
            "Would you like to DELETE /{mod_folder_name}/ and reinstall correctly for auto-update? [IAMSURE/n]: "
        )
        if input_str.lower() == "iamsure":
            git_remove_install(mod_folder_name, git_url)
