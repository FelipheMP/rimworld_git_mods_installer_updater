import sys
import os
import subprocess
import shutil
import time
import mods_list
import mods_list_formater


def mods_folder_verifier():
    curr_dir_name = os.path.basename(os.getcwd())
    if curr_dir_name != "Mods":
        print("\nPlace the scripts in your RimWorld/Mods/ folder before running it!")
        input("\nPress Enter to exit...")
        exit(0)


def is_file_empty(mods_py_path):
    return os.stat(mods_py_path).st_size == 0


def mods_list_verifier():
    completion_message = "Done!"
    mods_txt_path = "mods_list.txt"
    mods_py_path = "mods_list.py"

    if os.path.exists(mods_txt_path):
        mods_txt_mod_time = os.path.getmtime(mods_txt_path)

        if os.path.exists(mods_py_path):
            mods_py_mod_time = os.path.getmtime(mods_py_path)

            if is_file_empty(mods_py_path) or (mods_txt_mod_time > mods_py_mod_time):
                print(f"\n{mods_txt_path} file identified!")
                print(f"Sorting mods in {mods_txt_path} file alphabetically...")
                mods_list_formater.sorting_modslist_txt(mods_txt_path)
                print(f"Updating {mods_py_path} file...")
                mods_list_formater.process_file(mods_txt_path, mods_py_path)
                print(completion_message)
                exit(0)

    else:
        print(f"\n{mods_txt_path} file not found. Creating new example file...")
        with open(mods_txt_path, "w") as file:
            file.write(
                "PerformanceOptimizer https://github.com/Taranchuk/PerformanceOptimizer.git\n"
            )
            file.write(
                "JustPutItOverThere https://github.com/emipa606/JustPutItOverThere.git\n"
            )
            file.write("OwlAnimalGear https://github.com/Owlchemist/animal-gear.git\n")
        print(f"{mods_txt_path} file created!")
        print(f"Sorting mods in {mods_txt_path} file alphabetically...")
        print(completion_message)
        mods_list_formater.sorting_modslist_txt(mods_txt_path)
        print(
            "\nAdd mods by typing its name followed by its git repo url as is shown in the example file!"
        )
        print("To remove it, well, delete its name and url line.")
        print(
            "\nTip: You can create a file named blacklist.conf and add mod folder names in it."
        )
        print("Add each mod folder name in a new line.")
        print("Matching mod folder names will be ignored by the updater/installer!")
        print(f"\nUpdating {mods_py_path} file...")
        mods_list_formater.process_file(mods_txt_path, mods_py_path)
        print(completion_message)
        print("\nRun this script again to install/update the mods in the list.")
        exit(0)


def check_for_blacklist():
    return os.path.exists(BLACKLIST_CONFIG_FILE)


def dont_install():
    input_str = input("\nDo you want to check for updates only? [y/n]: ")
    return input_str.lower() == "y"


def blacklist_report():
    if os.path.exists(BLACKLIST_CONFIG_FILE):
        with open(BLACKLIST_CONFIG_FILE, "r") as file:
            print("\nBlacklist file detected! Mods below will be ignored:")
            print(file.read().strip())

        if input("\nDo you want to proceed? [y/n]: ").lower() != "y":
            print("Exiting...")
            exit(0)


def git_update(mod_folder_name, git_url):
    if check_for_blacklist():
        with open(BLACKLIST_CONFIG_FILE, "r") as file:
            for line in file:
                if mod_folder_name == line.strip():
                    return

    # Checking if mod is already installed.
    if os.path.exists(mod_folder_name) and not CHECK_UPDATES_ONLY:
        print(f"\n{mod_folder_name} is already installed. Skipping...")
        return

    if os.path.exists(mod_folder_name):
        print(f"\nUpdating {mod_folder_name}...")
        os.chdir(mod_folder_name)
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
            os.chdir("..")
            if not CHECK_UPDATES_ONLY:
                print(f"\n.git not found in /{mod_folder_name}/.")
                input_str = input(
                    "Would you like to DELETE /{mod_folder_name}/ and reinstall correctly for auto-update? [IAMSURE/n]: "
                )
                if input_str.lower() == "iamsure":
                    git_remove_install(mod_folder_name, git_url)
    else:
        if not CHECK_UPDATES_ONLY:
            input_str = input(
                f"\n/Mods/{mod_folder_name}/ folder not found. Would you like to install it? [y/n]: "
            )
            if input_str.lower() == "y":
                git_install(git_url)


def git_install(git_url):
    subprocess.run(["git", "clone", git_url])


def git_remove_install(mod_folder_name, git_url):
    input_str = input(
        f"\nDeleting and reinstalling mod /{mod_folder_name}/... Are you sure? [IAMSURE/n]: "
    )
    if input_str.lower() == "iamsure":
        shutil.rmtree(mod_folder_name)
        git_install(git_url)


def log_update(mod_folder_name):
    update_log_path = "update_log.txt"

    try:
        print(f"Attempting to log update for {mod_folder_name}")
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Fetch the timestamp of the last commit
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
        else:
            latest_commit_date, latest_commit_hour = "Unknown"

        if os.path.exists(update_log_path):
            with open(update_log_path, "a") as log_file:
                log_file.write(f"\n{mod_folder_name} was updated on {current_time}\n")
                log_file.write(
                    f"Latest commit date and hour: {latest_commit_date} {latest_commit_hour}\n"
                )
                log_file.write(
                    "------------------------------------------------------------------\n"
                )
        else:
            with open(update_log_path, "w") as log_file:
                log_file.write("Update History:\n")
                log_file.write(
                    "##################################################################\n"
                )
                log_file.write(f"\n{mod_folder_name} was updated on {current_time}\n")
                log_file.write(
                    f"Latest commit date and hour: {latest_commit_date} {latest_commit_hour}\n"
                )
                log_file.write(
                    "------------------------------------------------------------------\n"
                )
        print(f"Update for {mod_folder_name} logged successfully.")
    except Exception as e:
        print(f"Error logging update for {mod_folder_name}: {e}")


CHECK_UPDATES_ONLY = False
BLACKLIST_CONFIG_FILE = "blacklist.conf"

if __name__ == "__main__":
    mods_folder_verifier()
    mods_list_verifier()
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
            CHECK_UPDATES_ONLY = (
                True  # Sets to only update mods. Not installing new ones.
            )
        except ValueError:
            print("Invalid arguments. Using defaults.")

    # Calculate end index
    end_index = min(start_index + count, len(mods_list.mods))

    # Running the base script directly, it will ask if you want to install new mods.
    if not CHECK_UPDATES_ONLY:
        CHECK_UPDATES_ONLY = dont_install()

    # Slicing the mods list
    mods_to_update = mods_list.mods[start_index:end_index]

    for mod_folder_name, git_url in mods_to_update:
        git_update(mod_folder_name, git_url)

    print("\nMade with <3 by @FelipheMP")
    input("Press Enter to exit...")
