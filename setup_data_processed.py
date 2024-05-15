import os
import argparse
from utils.config_reader import read_config

def create_directory_structure(folder_name, overwrite=False):
    # Use the default path from configuration
    config = read_config()
    # Retrieve 'processed' directory path from the configuration
    processed_path = config['DIRECTORIES']['processed']

    # Join the folder_name with the processed_path
    target_path = os.path.join(processed_path, folder_name)

    # Define subdirectories
    subdirectories = ['ground_truth', 'input', 'segmentation']

    # Create main directory if not exists, or if overwrite is specified
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        print("Created main directory:", target_path)
    else:
        if overwrite:
            print("Overwriting main directory:", target_path)
        else:
            print("Main directory already exists:", target_path)

    # Create subdirectories
    for subdir in subdirectories:
        subdir_path = os.path.join(target_path, subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)
            print("Created subdirectory:", subdir_path)
        else:
            if overwrite:
                print("Overwriting subdirectory:", subdir_path)
            else:
                print("Subdirectory already exists:", subdir_path)

    # Print the structure in a styled manner
    print("#" * 20)
    print("Directory Structure for:", folder_name)
    print("#" * 20)
    for root, dirs, files in os.walk(target_path):
        level = root.replace(target_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
    print("#" * 20)

def main():
    parser = argparse.ArgumentParser(description="Create a directory structure for data preprocessing.")
    parser.add_argument('folders', nargs='*', help="List of folder names to create")
    parser.add_argument('-o', '--overwrite', action='store_true', help="Overwrite existing directories")

    args = parser.parse_args()
    
    if not args.folders:
        print("No folder names specified. Use --help for more information.")
    else:
        for folder in args.folders:
            create_directory_structure(folder, overwrite=args.overwrite)

if __name__ == "__main__":
    main()
