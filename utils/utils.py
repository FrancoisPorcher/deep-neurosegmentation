import os
import logging
from pathlib import Path

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def erase_files_and_optionally_directories_recursively(path, delete_directories=False):
    """
    Recursively erases all files within a given directory path and optionally deletes the directories themselves.

    :param path: The root directory path from where files and optionally directories will be deleted.
    :param delete_directories: Boolean indicating whether to delete directories after clearing them. Default is False.
    """
    # Convert the path to a Path object for easier manipulation
    root_path = Path(path)

    # Check if the given path is indeed a directory
    if not root_path.is_dir():
        logging.error(f"The path {root_path} is not a valid directory.")
        return

    try:
        for item in sorted(root_path.rglob('*'), key=lambda x: x.is_file(), reverse=True):
            # Deletes files
            if item.is_file():
                item.unlink()
                logging.info(f"File {item} has been deleted.")
            # If the option is enabled and the item is a directory, delete it after its files have been deleted
            elif item.is_dir() and delete_directories:
                # Ensure the directory is empty before attempting to delete
                if not any(item.iterdir()):
                    item.rmdir()
                    logging.info(f"Directory {item} has been deleted.")

        if delete_directories and root_path.is_dir() and not any(root_path.iterdir()):
            # Optionally, delete the root directory itself if it's now empty and the option is enabled
            root_path.rmdir()
            logging.info(f"Root directory {root_path} has been deleted.")

        logging.info("Operation completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Example usage

