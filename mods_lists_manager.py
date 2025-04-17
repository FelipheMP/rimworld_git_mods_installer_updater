import os
import mods_list_formater
import utils


def verify_mods_folder():
    """Verify if the script is running in the correct directory."""
    curr_dir_name = os.path.basename(os.getcwd())
    if curr_dir_name != "Mods":
        print("\nPlace the scripts in your RimWorld/Mods/ folder before running it!")
        input("\nPress Enter to exit...")
        exit(0)


def verify_mods_list(mods_txt_path: str, mods_py_path: str, completion_message: str):
    """
    Verify and update the mods list files.
    Args:
        mods_txt_path (str): Path to the mods.txt file.
        mods_py_path (str): Path to the mods.py file.
        completion_message (str): Message to display upon completion.
    """
    verify_mods_folder()
    try:
        if os.path.exists(mods_txt_path):
            mods_txt_mod_time = os.path.getmtime(mods_txt_path)

            if os.path.exists(mods_py_path):
                mods_py_mod_time = os.path.getmtime(mods_py_path)

                with open(mods_py_path, "r") as file:
                    mods_py_content = file.read()

                if (
                    utils.is_file_empty(mods_py_path)
                    or (mods_txt_mod_time > mods_py_mod_time)
                    or "mods: List[Tuple[str, str]] = []" in mods_py_content
                ):
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
                file.write(
                    "OwlAnimalGear https://github.com/Owlchemist/animal-gear.git\n"
                )
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
    except (FileNotFoundError, PermissionError) as e:
        print(f"\nError accessing mods list files: {e}")
    except Exception as e:
        print(f"\nUnexpected error verifying mods lists: {e}")
