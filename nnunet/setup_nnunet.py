import os  # Importing the os module to interact with the operating system
import shutil  # Importing shutil for high-level file operations
from pathlib import Path  # Importing Path from pathlib to handle file system paths
import configparser  # Importing configparser to manage configuration files
from argparse import ArgumentParser  # Importing ArgumentParser for command-line argument parsing
from tqdm import tqdm  # Importing tqdm to display progress bars
import json  # Importing json to handle JSON data

def setup_nnunet_structure(config, config_path):
    """
    Create general nnU-Net directories and update the configuration file.

    Args:
        config (configparser.ConfigParser): The configuration parser object.
        config_path (str): The path to the configuration file.
    """
    print("=" * 60)
    print("Setting up nnUNet Paths")
    print("=" * 60)
    print(f"Path for nnU-Net: {nnunet_path}")
    print("-" * 60)
    print(f"Path for Raw folder: {raw_folder}")
    print(f"Path for Preprocessed folder: {preprocessed_folder}")
    print(f"Path for Results folder: {results_folder}")
    print("=" * 60)

    # Ensuring base folders exist
    raw_folder.mkdir(parents=True, exist_ok=True)
    preprocessed_folder.mkdir(parents=True, exist_ok=True)
    results_folder.mkdir(parents=True, exist_ok=True)
    print("General nnUNet folders created successfully.\n")
    
    # Update config.ini file with the new paths
    config.set('DIRECTORIES', 'nnUNet_raw', str(raw_folder))
    config.set('DIRECTORIES', 'nnUNet_preprocessed', str(preprocessed_folder))
    config.set('DIRECTORIES', 'nnUNet_results', str(results_folder))
    
    # Writing changes back to config file
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    
    print("Configuration file updated with new paths.")

def setup_mindboggle_json(dataset_folder):
    """
    Create a dataset.json file for the Mindboggle dataset within the specified dataset folder.

    Args:
        dataset_folder (Path): The path to the dataset folder.
    """
    data = {
        "channel_names": {
            "0": "T1"
        },      
        "labels": {
            "background": 0,
            "Cortical gray matter": 1,
            "Cortical White matter": 2,
            "Cerebellum gray": 3,
            "Cerebellum white": 4
        },
        "numTraining": 101, 
        "file_ending": ".nii.gz",
        "overwrite_image_reader_writer": "SimpleITKIO"  # Optional, auto-detected if not specified
    }

    # Path to the JSON file within the dataset folder
    json_path = dataset_folder / "dataset.json"
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"dataset.json created at {json_path}")

def copy_files_to_dataset(src_path, dest_folder, file_type):
    """
    Copy files from source path to destination folder with progress display.

    Args:
        src_path (str): The source directory path.
        dest_folder (Path): The destination directory path.
        file_type (str): The type of files being copied (e.g., 'input images to training').
    """
    print("=" * 60)
    print(f"COPYING {file_type.upper()} FILES")
    print("=" * 60)
    files = list(Path(src_path).glob('*'))  # Listing all files in the source directory
    for src_file in tqdm(files, desc=f"Copying {file_type}"):
        shutil.copy(src_file, dest_folder)  # Copying each file to the destination directory
        print(f"Copied {src_file.name} to {dest_folder}")
    print("=" * 60 + "\n")

def setup_mindboggle_dataset():
    """
    Setup specific dataset folder within the nnU-Net structure and copy necessary files.
    """
    print("=" * 60)
    print("Setting up Mindboggle Dataset")
    print("=" * 60)

    # Creating specific dataset folder
    dataset_folder = raw_folder / "Dataset001_mindboggle"
    imagesTr_folder = dataset_folder / "imagesTr"
    imagesTs_folder = dataset_folder / "imagesTs"
    labelsTr_folder = dataset_folder / "labelsTr"

    # Create dataset directories
    dataset_folder.mkdir(exist_ok=True)
    imagesTr_folder.mkdir(exist_ok=True)
    imagesTs_folder.mkdir(exist_ok=True)
    labelsTr_folder.mkdir(exist_ok=True)

    # Copy files to corresponding folders
    copy_files_to_dataset(mindboggle_input_path, imagesTr_folder, 'input images to training')
    copy_files_to_dataset(mindboggle_input_path, imagesTs_folder, 'input images to testing')
    copy_files_to_dataset(mindboggle_segmentation_path, labelsTr_folder, 'segmentation')
    
    rename_images_and_labels_for_nnunet_convention("mindboggle", imagesTr_folder, labelsTr_folder, imagesTs_folder)
    
    # Create the JSON file for dataset description
    setup_mindboggle_json(dataset_folder)
    
    print("Mindboggle dataset folders populated successfully.")

def rename_images_and_labels_for_nnunet_convention(dataset_name, input_directory, label_directory, test_directory):
    """
    Rename images and labels to follow nnU-Net convention.

    Args:
        dataset_name (str): The name of the dataset.
        input_directory (Path): The directory containing the input images.
        label_directory (Path): The directory containing the label images.
        test_directory (Path): The directory containing the test images.
    """
    # Get the list of files in the input directory
    train_file_names = sorted(os.listdir(input_directory))
    test_file_names = sorted(os.listdir(test_directory))
    label_file_names = sorted(os.listdir(label_directory))

    print("Renaming files for nnU-Net convention")
    print("There are {} files in the input directory".format(len(train_file_names)))
    print("There are {} files in the test directory".format(len(test_file_names)))
    print("There are {} files in the label directory".format(len(label_file_names)))

    # Rename training files
    for i, file_name in enumerate(train_file_names):
        # Extract the file extension and base name
        file_extension = file_name.split('.')[-1]
        base_name = file_name[:-7]  # Assuming .nii.gz

        # Define new file names according to nnU-Net convention
        new_input_file_name = f"{dataset_name}_{str(i).zfill(4)}_0000.nii.gz"
        new_label_file_name = f"{dataset_name}_{str(i).zfill(4)}.nii.gz"

        # Full paths for renaming
        input_file_path = input_directory / file_name
        label_file_path = label_directory / f"{base_name}.nii.gz"
        new_input_file_path = input_directory / new_input_file_name
        new_label_file_path = label_directory / new_label_file_name

        # Rename the input file
        os.rename(input_file_path, new_input_file_path)
        # Check if corresponding label file exists and rename it
        if label_file_path.exists():
            os.rename(label_file_path, new_label_file_path)

        # Print out the renaming actions
        print(f"Renamed {file_name} to {new_input_file_name} (input) and {base_name}.nii.gz to {new_label_file_name} (label)")

    # Rename test files
    for i, file_name in enumerate(test_file_names):
        # Extract the file extension and base name
        file_extension = file_name.split('.')[-1]
        base_name = file_name[:-7]  # Assuming .nii.gz

        # Define new file name according to nnU-Net convention
        new_file_name = f"{dataset_name}_{str(i).zfill(4)}_0000.nii.gz"

        # Full path for renaming
        input_file_path = test_directory / file_name
        new_input_file_path = test_directory / new_file_name

        # Rename the input file
        os.rename(input_file_path, new_input_file_path)

        # Print out the renaming actions
        print(f"Renamed {file_name} to {new_file_name} (input)")

    print("Successfully renamed all files")

# Command line argument parsing
parser = ArgumentParser(description="Setup nnU-Net structure and manage specific datasets.")
parser.add_argument("--mindboggle", action="store_true", help="Setup for the Mindboggle dataset")
args = parser.parse_args()

# Reading configuration
config = configparser.ConfigParser()
config_path = '/home/fp427/rds/rds-cam-segm-7tts6phZ4tw/deep-neurosegmentation/config.ini'  # ensure this path is correct
config.read(config_path)

# Define directories from config
nnunet_path = config['DIRECTORIES']['nnunet']
raw_folder = Path(nnunet_path, "nnUNet_raw")
preprocessed_folder = Path(nnunet_path, "nnUNet_preprocessed")
results_folder = Path(nnunet_path, "nnUNet_results")
mindboggle_path = config['DIRECTORIES']['mindboggle']
mindboggle_input_path = os.path.join(mindboggle_path, 'input')
mindboggle_segmentation_path = os.path.join(mindboggle_path, 'segmentation')

# Always perform general setup
setup_nnunet_structure(config=config, config_path=config_path)

# Additional setup for Mindboggle if specified
if args.mindboggle:
    setup_mindboggle_dataset()
