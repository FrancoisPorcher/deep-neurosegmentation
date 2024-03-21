import os
import shutil
import sys
from pathlib import Path

# Assuming notebooks are one level deep in the project structure
sys.path.insert(0, str(Path.cwd().parent))

from config import config

def add_iteration_i_to_name(filename, i):
    """
    Correctly adds '_iteration_1' before the '.nii' extension of the given filename,
    specifically handling files that end with '.nii.gz'.

    :param filename: The original filename
    :return: The modified filename with '_iteration_1' added correctly before the '.nii' extension
    """
    # Check if the filename ends with '.nii.gz'
    if filename.endswith('.nii.gz'):
        # Insert '_iteration_1' before '.nii.gz'
        new_name = filename[:-7] + '_iteration_' + str(i) + '.nii.gz'
        return new_name
    else:
        print(f"Filename {filename} does not end with '.nii.gz'")
    

def copy_and_rename_files_with_iteration(input_path, output_path, iteration_number):
    """
    Copies files from the input path to the output path, renaming them to include an iteration number.

    :param input_path: The directory to copy files from
    :param output_path: The directory to copy files to
    :param iteration_number: The iteration number to add to the filenames
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # List all files in the input directory
    for filename in sorted(os.listdir(input_path)):
        # Generate the new filename with the iteration number
        if filename.endswith('.nii.gz'):
            new_filename = add_iteration_i_to_name(filename, iteration_number)

            # Define the old and new file paths
            old_file_path = os.path.join(input_path, filename)
            new_file_path = os.path.join(output_path, new_filename)

            # Copy the file from the old path to the new path
            if os.path.isfile(old_file_path):  # Ensure it's a file, not a directory
                shutil.copy2(old_file_path, new_file_path)
                print(f"Copied and renamed {filename} to {new_filename}")
        else:
            print(f"Filename {filename} does not end with '.nii.gz'")
            
def process_dbb_files(output_path):
    # Assuming `config` is accessible within this function
    iterations = [(config.ITERATION_1_PATH, 1), (config.ITERATION_2_PATH, 2), (config.ITERATION_3_PATH, 3)]

    for input_path, iteration_number in iterations:
        copy_and_rename_files_with_iteration(input_path, output_path, iteration_number)

        
        
if __name__ == '__main__':
    process_dbb_files(output_path = config.PROCESSED_DBB_DATA_PATH)