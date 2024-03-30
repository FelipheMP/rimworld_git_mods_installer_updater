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

def mods_list_verifier():
    mods_txt_path = "mods_list.txt"
    mods_py_path = "mods_list.py"

    if os.path.exists(mods_txt_path):
        mods_list_mod_time = os.path.getmtime(mods_txt_path)

        if os.path.exists(mods_py_path):
            mods_py_mod_time = os.path.getmtime(mods_py_path)

            if mods_list_mod_time > mods_py_mod_time:
                print(f"\n{mods_txt_path} file modified!")
                print(f"Updating {mods_py_path} file...")
                mods_list_formater.process_file(mods_txt_path, mods_py_path)
                print("Done!")
                exit(0)

    else:
        print(f"\n{mods_txt_path} file not found. Creating new example file...")
        with open(mods_txt_path, "w") as file:
            file.write("PerformanceOptimizer https://github.com/Taranchuk/PerformanceOptimizer.git\n")
            file.write("JustPutItOverThere https://github.com/emipa606/JustPutItOverThere.git\n")
            file.write("OwlAnimalGear https://github.com/Owlchemist/animal-gear.git\n")
            file.write("WarhammerGor https://github.com/emipa606/WarhammerGor.git\n")
            file.write("MoharFramework https://github.com/goudaQuiche/MoharFramework.git\n")
        print("Mods list file created!")
        print("\nAdd mods by typing its name followed by its git repo url as is shown in the example file!")
        print("To remove it, well, delete its name and url line.")
        print("\nTip: You can create a file named blacklist.conf and add mod folder names in it.")
        print("Add each mod folder name in a new line.")
        print("Matching mod folder names will be ignored by the updater/installer!")
        print(f"\nUpdating {mods_py_path} file...")
        mods_list_formater.process_file(mods_txt_path, mods_py_path)
        print("Done!")
        print("\nRun this script again to install/update the mods in the list.")
        exit(0)

def check_for_blacklist():
    if os.path.exists("blacklist.conf"):
        return True
    else:
        return False

def dont_install():
    global DONT_INSTALL
    input_str = input("\nDo you want to check for updates only? [y/n]: ")
    if input_str.lower() == "y":
        DONT_INSTALL = True

def blacklist_report():
    if os.path.exists("blacklist.conf"):
        with open("blacklist.conf", "r") as file:
            print("\nBlacklist file detected! Below mods will be ignored:")
            for line in file:
                print(line.strip())
            input_str = input("\nDo you want to proceed? [y/n]: ")
            if input_str.lower() == "y":
                return
            else:
                exit(0)

def git_update(mod_folder_name, git_url):
    if check_for_blacklist():
        with open("blacklist.conf", "r") as file:
            for line in file:
                if mod_folder_name == line.strip():
                    return

    if os.path.exists(f"{mod_folder_name}-master"):
        mod_folder_name += "-master"

    if os.path.exists(mod_folder_name):
        print(f"\nUpdating {mod_folder_name}...")
        os.chdir(mod_folder_name)
        if os.path.exists(".git"):
            subprocess.run(["git", "fetch"])
            result = subprocess.run(["git", "pull"], capture_output = True, text = True)
            if "Already up to date." not in result.stdout:
                os.chdir("..")
                log_update(mod_folder_name)
            else:
                print("Already up to date!")
            os.chdir("..")
        else:
            os.chdir("..")
            if not DONT_INSTALL:
                print(f"\n.git not found in /{mod_folder_name}/.")
                input_str = input("Would you like to DELETE /{mod_folder_name}/ and reinstall correctly for auto-update? [IAMSURE/n]: ")
                if input_str.lower() == "iamsure":
                    git_remove_install(mod_folder_name, git_url)
    else:
        if not DONT_INSTALL:
            input_str = input(f"\n/Mods/{mod_folder_name}/ folder not found. Would you like to install? [y/n]: ")
            if input_str.lower() == "y":
                git_install(git_url)

def git_install(git_url):
    subprocess.run(["git", "clone", git_url])

def git_remove_install(mod_folder_name, git_url):
    input_str = input(f"\nDeleting and reinstalling mod /{mod_folder_name}/... Are you sure? [IAMSURE/n]: ")
    if input_str.lower() == "iamsure":
        shutil.rmtree(mod_folder_name)
        git_install(git_url)

def log_update(mod_folder_name):
    update_log_path = "update_log.txt"

    try:
        print(f"Attempting to log update for {mod_folder_name}")
        current_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        mod_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(os.path.getmtime(mod_folder_name)))
        
        if os.path.exists(update_log_path):
            with open(update_log_path, "a") as log_file:
                log_file.write(f"\n{mod_folder_name} was updated on {current_time}\n")
                log_file.write(f"Last modification time: {mod_time}\n")
                log_file.write("------------------------------------------------------------------\n")
        else:
            with open(update_log_path, "w") as log_file:
                log_file.write("Update History:\n")
                log_file.write("##################################################################\n")
                log_file.write(f"\n{mod_folder_name} was updated on {current_time}\n")
                log_file.write(f"Last modification time: {mod_time}\n")
                log_file.write("------------------------------------------------------------------\n")
    except Exception as e:
        print(f"Error logging update for {mod_folder_name}: {e}")

DONT_INSTALL = False

if __name__ == "__main__":
    mods_folder_verifier()
    mods_list_verifier()
    dont_install()
    check_for_blacklist()
    blacklist_report()

    for mod_folder_name, git_url in mods_list.mods:
        git_update(mod_folder_name, git_url)

    input("\nPress Enter to exit...")

# Made with <3 by github.com/BiP213! Enjoy! :D