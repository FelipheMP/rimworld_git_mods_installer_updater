import git_operations


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
            git_operations.git_install(git_url)
        else:
            print(f"Skipping {mod_folder_name} installation.")
            return
    except Exception as e:
        print(f"\nError reading input: {e}")
