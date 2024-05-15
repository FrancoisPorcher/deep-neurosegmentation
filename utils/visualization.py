import os
import random
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def print_header_footer(message, length=30, char='='):
    print(char * length)
    print(message)
    print(char * length)

def print_subheader(message, length=30, char='-'):
    print(char * length)
    print(message)
    print(char * length)


def get_random_file_paths(base_dir):
    # Get a list of all files in the input directory
    input_dir = os.path.join(base_dir, 'input')
    file_names = os.listdir(input_dir)

    # Choose a random file name
    random_file = random.choice(file_names)

    # Construct the paths for the corresponding files in all three directories
    input_path = os.path.join(input_dir, random_file)
    ground_truth_path = os.path.join(base_dir, 'ground_truth', random_file)
    segmentation_path = os.path.join(base_dir, 'segmentation', random_file)

    # Print
    print_header_footer("Getting a random file from directory")
    print(f"Random file: {random_file}")
    print_subheader(f"Input path: {input_path}")
    print(f"Ground truth path: {ground_truth_path}")
    print(f"Segmentation path: {segmentation_path}")
    print_header_footer("", 30, "=")
    print("\n\n")  # skip 3 lines

    return ground_truth_path, input_path, segmentation_path

def load_nifti_file(file_path, file_type):
    if file_path is not None:
        img = nib.load(file_path)
        data = img.get_fdata()
        print(f"{file_type} Data (from {file_path}):")
        print(f"Shape: {data.shape}")
        return data
    else:
        print(f"{file_type} path is not provided.")
        return None

def load_nifti_triplet(ground_truth_path=None, input_path=None, segmentation_path=None):
    # Print
    print_header_footer("Loading nifti files..")

    # Load ground truth file
    ground_truth_data = load_nifti_file(ground_truth_path, "Ground Truth")
    print_subheader("")

    # Load input file
    input_data = load_nifti_file(input_path, "Input")
    print_subheader("")

    # Load segmentation file
    segmentation_data = load_nifti_file(segmentation_path, "Segmentation")
    print_header_footer("")
    print("\n\n")  # skip 3 lines

    return ground_truth_data, input_data, segmentation_data

def report_data_info(ground_truth_data, input_data, segmentation_data):
    print_header_footer("Data Information")

    print("\nGround Truth Data:")
    print_subheader("")
    print(f"Data Type: {ground_truth_data.dtype}")
    print(f"Number of Unique Values: {len(np.unique(ground_truth_data))}")

    print("\nInput Data:")
    print_subheader("")
    print(f"Data Type: {input_data.dtype}")
    print(f"Number of Unique Values: {len(np.unique(input_data))}")

    print("\nSegmentation Data:")
    print_subheader("")
    print(f"Data Type: {segmentation_data.dtype}")
    print(f"Number of Unique Values: {len(np.unique(segmentation_data))}")

    print_header_footer("")
    print("\n\n")  # skip 3 lines

    # Plot the distribution of values
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    # Ground Truth Data
    axes[0].hist(ground_truth_data.ravel(), bins=np.unique(ground_truth_data).shape[0])
    axes[0].set_title('Ground Truth Data')

    # Input Data
    axes[1].hist(input_data.ravel(), bins=100)
    axes[1].set_title('Input Data')

    # Segmentation Data
    unique_segmentation_values = np.unique(segmentation_data)
    axes[2].hist(segmentation_data.ravel(), bins=unique_segmentation_values.shape[0], align='left')
    axes[2].set_xticks(unique_segmentation_values)
    axes[2].set_title('Segmentation Data')

    fig.tight_layout()
    plt.show()

