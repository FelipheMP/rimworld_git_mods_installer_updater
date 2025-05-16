import sys
import json
import git_operations
import mods_list
import mods_lists_manager
import user_interactions
import utils


# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)
BLACKLIST_FILE_PATH = config["blacklist"]
MODS_PY_PATH = config["mods_py"]
MODS_TXT_PATH = config["mods_txt"]
UPDATE_LOG_PATH = config["update_log"]


COMPLETION_MESSAGE = "Done!"
is_check_updates_only: bool = False


# Main script
if __name__ == "__main__":
    mods_lists_manager.verify_mods_list(MODS_TXT_PATH, MODS_PY_PATH, COMPLETION_MESSAGE)
    utils.check_for_blacklist(BLACKLIST_FILE_PATH)
    utils.blacklist_report(BLACKLIST_FILE_PATH)

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
            is_check_updates_only = bool(user_interactions.ask_update_mode())

    # Calculate end index
    end_index = min(start_index + count, len(mods_list.mods))

    # Slicing the mods list
    mods_to_update = mods_list.mods[start_index:end_index]

    for mod_folder_name, git_url in mods_to_update:
        git_operations.git_update(
            mod_folder_name, git_url, BLACKLIST_FILE_PATH, UPDATE_LOG_PATH, is_check_updates_only
        )

    print(f"\n{COMPLETION_MESSAGE}")

    print("\nMade with <3 by @FelipheMP")
    input("Press Enter to exit...")
