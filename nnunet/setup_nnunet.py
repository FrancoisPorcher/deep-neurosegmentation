import os
import shutil
from pathlib import Path
import configparser
from argparse import ArgumentParser
from tqdm import tqdm
import json

def print_header_footer(message, length=60, char='='):
    print(char * length)
    print(message)
    print(char * length)

def print_subheader(message, length=60, char='-'):
    print(char * length)
    print(message)
    print(char * length)

def setup_nnunet_structure(config, config_path):
    """
    Create general nnU-Net directories and update the configuration file.

    Args:
        config (configparser.ConfigParser): The configuration parser object.
        config_path (str): The path to the configuration file.
    """
    nnunet_path = config['DIRECTORIES']['nnunet']
    raw_folder = Path(nnunet_path, "nnUNet_raw")
    preprocessed_folder = Path(nnunet_path, "nnUNet_preprocessed")
    results_folder = Path(nnunet_path, "nnUNet_results")

    print_header_footer("Setting up nnUNet Paths")
    print(f"Path for nnU-Net: {nnunet_path}")
    print_subheader(f"Path for Raw folder: {raw_folder}")
    print(f"Path for Preprocessed folder: {preprocessed_folder}")
    print(f"Path for Results folder: {results_folder}")
    print_header_footer("")

    raw_folder.mkdir(parents=True, exist_ok=True)
    preprocessed_folder.mkdir(parents=True, exist_ok=True)
    results_folder.mkdir(parents=True, exist_ok=True)
    print("General nnUNet folders created successfully.\n")
    
    config.set('DIRECTORIES', 'nnUNet_raw', str(raw_folder))
    config.set('DIRECTORIES', 'nnUNet_preprocessed', str(preprocessed_folder))
    config.set('DIRECTORIES', 'nnUNet_results', str(results_folder))
    
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    
    print("Configuration file updated with new paths.")

def setup_mindboggle_json(dataset_folder):
    """
    Create a dataset.json file for the MindBoggle dataset within the dataset folder.

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
        "overwrite_image_reader_writer": "SimpleITKIO"
    }

    json_path = dataset_folder / "dataset.json"
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"dataset.json created at {json_path}")

def setup_dbb_json(dataset_folder):
    """
    Create a dataset.json file for the DBB dataset within the dataset folder.

    Args:
        dataset_folder (Path): The path to the dataset folder.
    """
    data = {
        "channel_names": {
            "0": "T1"
        },
        "labels": {
            "background": 0,
            "CSF": 1,
            "Gray Matter": 2,
            "White Matter": 3,
            "Subcortical Gray Matter": 4,
            "Brain Stem": 5,
            "Cerebellum": 6
        },
        "numTraining": 954,
        "file_ending": ".nii.gz",
        "overwrite_image_reader_writer": "SimpleITKIO"
    }

    json_path = dataset_folder / "dataset.json"
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"dataset.json created at {json_path}")



def setup_feta_json(dataset_folder):
    """
    Create a dataset.json file for the FeTA dataset within the dataset folder.

    Args:
        dataset_folder (Path): The path to the dataset folder.
    """
    data = {
        "channel_names": {
            "0": "T2"
        },
        "labels": {
            "background and non-brain tissue": 0,
            "cerebrospinal fluid": 1,
            "gray matter": 2,
            "white matter": 3,
            "ventricles": 4,
            "cerebellum": 5,
            "deep gray matter": 6,
            "brainstem": 7
        },
        "numTraining": 80,
        "file_ending": ".nii.gz",
        "overwrite_image_reader_writer": "SimpleITKIO"
    }

    json_path = dataset_folder / "dataset.json"
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"dataset.json created at {json_path}")

def copy_files_to_dataset(src_path, dest_folder, file_type, overwrite=False):
    """
    Copy files from source path to destination folder with progress display.

    Args:
        src_path (str): The source directory path.
        dest_folder (Path): The destination directory path.
        file_type (str): The type of files being copied (e.g., 'input images to training').
        overwrite (bool): Whether to overwrite existing files.
    """
    print_header_footer(f"COPYING {file_type.upper()} FILES")
    files = list(Path(src_path).glob('*'))
    for src_file in tqdm(files, desc=f"Copying {file_type}"):
        dest_file = dest_folder / src_file.name
        if overwrite or not dest_file.exists():
            shutil.copy(src_file, dest_folder)
            print(f"Copied {src_file.name} to {dest_folder}")
        else:
            print(f"Skipped {src_file.name} (already exists)")
    print_header_footer("")

def setup_dataset(dataset_name, input_path, segmentation_path, overwrite=False):
    """
    Setup specific dataset folder within the nnU-Net structure and copy necessary files.

    Args:
        dataset_name (str): The name of the dataset (e.g., "mindboggle", "dbb", "dbb_augmented", "feta").
        input_path (str): The path to the input images.
        segmentation_path (str): The path to the segmentation images.
        overwrite (bool): Whether to overwrite existing files.
    """
    dataset_id_map = {
        "mindboggle": 1,
        "dbb": 2,
        "feta": 4
    }
    dataset_id = dataset_id_map[dataset_name]

    print_header_footer(f"Setting up {dataset_name.capitalize()} Dataset (ID: {dataset_id})")

    dataset_folder = raw_folder / f"Dataset00{dataset_id}_{dataset_name}"
    imagesTr_folder = dataset_folder / "imagesTr"
    imagesTs_folder = dataset_folder / "imagesTs"
    labelsTr_folder = dataset_folder / "labelsTr"

    dataset_folder.mkdir(exist_ok=True)
    imagesTr_folder.mkdir(exist_ok=True)
    imagesTs_folder.mkdir(exist_ok=True)
    labelsTr_folder.mkdir(exist_ok=True)

    copy_files_to_dataset(input_path, imagesTr_folder, 'input images to training', overwrite)
    copy_files_to_dataset(input_path, imagesTs_folder, 'input images to testing', overwrite)
    copy_files_to_dataset(segmentation_path, labelsTr_folder, 'segmentation', overwrite)
    
    rename_images_and_labels_for_nnunet_convention(dataset_name, imagesTr_folder, labelsTr_folder, imagesTs_folder)
    
    json_setup_functions = {
        "mindboggle": setup_mindboggle_json,
        "dbb": setup_dbb_json,
        "feta": setup_feta_json
    }
    json_setup_functions[dataset_name](dataset_folder)
    
    print(f"{dataset_name.capitalize()} dataset folders populated successfully.")

def rename_images_and_labels_for_nnunet_convention(dataset_name, input_directory, label_directory, test_directory):
    """
    Rename images and labels to follow nnU-Net convention.

    Args:
        dataset_name (str): The name of the dataset.
        input_directory (Path): The directory containing the input images.
        label_directory (Path): The directory containing the label images.
        test_directory (Path): The directory containing the test images.
    """
    train_file_names = sorted(os.listdir(input_directory))
    test_file_names = sorted(os.listdir(test_directory))
    label_file_names = sorted(os.listdir(label_directory))

    print("Renaming files for nnU-Net convention")
    print(f"There are {len(train_file_names)} files in the input directory")
    print(f"There are {len(test_file_names)} files in the test directory")
    print(f"There are {len(label_file_names)} files in the label directory")

    for i, file_name in enumerate(train_file_names):
        base_name = file_name[:-7]  # Assuming .nii.gz

        new_input_file_name = f"{dataset_name}_{str(i).zfill(4)}_0000.nii.gz"
        new_label_file_name = f"{dataset_name}_{str(i).zfill(4)}.nii.gz"

        input_file_path = input_directory / file_name
        label_file_path = label_directory / f"{base_name}.nii.gz"
        new_input_file_path = input_directory / new_input_file_name
        new_label_file_path = label_directory / new_label_file_name

        os.rename(input_file_path, new_input_file_path)
        if label_file_path.exists():
            os.rename(label_file_path, new_label_file_path)

        print(f"Renamed {file_name} to {new_input_file_name} (input) and {base_name}.nii.gz to {new_label_file_name} (label)")

    for i, file_name in enumerate(test_file_names):
        base_name = file_name[:-7]  # Assuming .nii.gz

        new_file_name = f"{dataset_name}_{str(i).zfill(4)}_0000.nii.gz"

        input_file_path = test_directory / file_name
        new_input_file_path = test_directory / new_file_name

        os.rename(input_file_path, new_input_file_path)

        print(f"Renamed {file_name} to {new_file_name} (input)")

    print("Successfully renamed all files")

def main():
    parser = ArgumentParser(description="Setup nnU-Net structure and manage specific datasets.")
    parser.add_argument("--mindboggle", action="store_true", help="Setup for the Mindboggle dataset")
    parser.add_argument("--dbb", action="store_true", help="Setup for the DBB dataset")
    parser.add_argument("--feta", action="store_true", help="Setup for the Feta dataset")
    parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config_path = '/home/fp427/rds/rds-cam-segm-7tts6phZ4tw/deep-neurosegmentation/config.ini'
    config.read(config_path)

    global raw_folder
    nnunet_path = config['DIRECTORIES']['nnunet']
    raw_folder = Path(nnunet_path, "nnUNet_raw")
    preprocessed_folder = Path(nnunet_path, "nnUNet_preprocessed")
    results_folder = Path(nnunet_path, "nnUNet_results")
    
    setup_nnunet_structure(config=config, config_path=config_path)

    dataset_name_map = {
        "mindboggle": 1,
        "dbb": 2,
        "feta": 4
    }

    selected_datasets = [k for k, v in vars(args).items() if k in dataset_name_map and v]
    if not selected_datasets:
        selected_datasets = ["mindboggle", "dbb", "feta"]  # Default datasets

    for dataset_name in selected_datasets:
        input_path = os.path.join(config['DIRECTORIES'][dataset_name], 'input')
        segmentation_path = os.path.join(config['DIRECTORIES'][dataset_name], 'segmentation')
        setup_dataset(dataset_name, input_path, segmentation_path, args.overwrite)

if __name__ == "__main__":
    main()
