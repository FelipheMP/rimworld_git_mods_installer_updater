import os
import time
import subprocess


def fetch_latest_commit_timestamp(mod_folder_name: str) -> tuple[str, str]:
    try:
        timestamp = subprocess.check_output(
            ["git", "show", "--format=%ci", "HEAD"],
            cwd=mod_folder_name,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        date, hour = timestamp.split(" ")[:2]
        return date, hour
    except subprocess.CalledProcessError:
        return "Unknown", "Unknown"


def log_update(mod_folder_name: str, update_log_path: str) -> None:
    try:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        latest_commit_date, latest_commit_hour = fetch_latest_commit_timestamp(
            mod_folder_name
        )

        log_entry = (
            f"\n{mod_folder_name} was updated on {current_time}\n"
            f"Latest commit date and hour: {latest_commit_date} {latest_commit_hour}\n"
            "------------------------------------------------------------------\n"
        )

        mode = "a" if os.path.exists(update_log_path) else "w"
        with open(update_log_path, mode) as log_file:
            if mode == "w":
                log_file.write("Update History:\n")
                log_file.write(
                    "##################################################################\n"
                )
            log_file.write(log_entry)

        print(f"\nUpdate for {mod_folder_name} logged successfully")
    except FileNotFoundError:
        print("\nLog file path does not exist.")
    except PermissionError:
        print("\nPermission denied to write to the log file.")
    except Exception as e:
        print(f"Error logging update: {e}")
