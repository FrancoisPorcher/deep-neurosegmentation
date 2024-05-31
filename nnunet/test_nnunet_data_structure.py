import configparser
import json
from pathlib import Path

def read_and_print_config(config_path='/home/fp427/rds/rds-cam-segm-7tts6phZ4tw/deep-neurosegmentation/config.ini'):
    # Read the config file
    config = configparser.ConfigParser()
    config.read(config_path)

    # Get the required directories from the config file
    nnunet_path = config['DIRECTORIES']['nnunet']
    nnUNet_raw = Path(nnunet_path, "nnUNet_raw")
    nnUNet_preprocessed = Path(nnunet_path, "nnUNet_preprocessed")
    nnUNet_results_folder = Path(nnunet_path, "nnUNet_results")

    def check_dataset(dataset_name, dataset_id):
        dataset_path = Path(nnunet_path, "nnUNet_raw", f"Dataset{dataset_id:03d}_{dataset_name}")
        
        dataset_json = dataset_path / 'dataset.json'
        imagesTr = dataset_path / 'imagesTr'
        imagesTs = dataset_path / 'imagesTs'
        labelsTr = dataset_path / 'labelsTr'

        imagesTr_count = len(list(imagesTr.glob('*'))) if imagesTr.exists() else 0
        imagesTs_count = len(list(imagesTs.glob('*'))) if imagesTs.exists() else 0
        labelsTr_count = len(list(labelsTr.glob('*'))) if labelsTr.exists() else 0

        numTraining = None
        if dataset_json.exists():
            with open(dataset_json, 'r') as f:
                data = json.load(f)
                numTraining = data.get('numTraining', None)

        print(f"######" * 20)
        print(f"{dataset_name} dataset: {dataset_path}")
        print(f"dataset_json: {dataset_json}")
        print(f"imagesTr: {imagesTr} (file count: {imagesTr_count})")
        print(f"imagesTs: {imagesTs} (file count: {imagesTs_count})")
        print(f"labelsTr: {labelsTr} (file count: {labelsTr_count})")
        print(f"numTraining: {numTraining} (should match imagesTr_count: {imagesTr_count})")

    # Check each dataset
    check_dataset("mindboggle", 1)
    check_dataset("dbb", 2)
    check_dataset("feta", 4)

    # Print the directories
    print(f"nnUNet_raw: {nnUNet_raw}")
    print(f"nnUNet_preprocessed: {nnUNet_preprocessed}")
    print(f"nnUNet_results_folder: {nnUNet_results_folder}")
    print("######" * 20)

# Call the function
read_and_print_config()
