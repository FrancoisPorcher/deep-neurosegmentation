import os
import random
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def get_random_file_paths(base_dir):
    # Get a list of all files in the first directory
    first_dir = os.path.join(base_dir, 'ground_truth')
    file_names = os.listdir(first_dir)

    # Choose a random file name
    random_file = random.choice(file_names)

    # Construct the paths for the corresponding files in all three directories
    ground_truth_path = os.path.join(first_dir, random_file)
    input_path = os.path.join(base_dir, 'input', random_file)
    segmentation_path = os.path.join(base_dir, 'segmentation', random_file)

    # Print
    print("=" * 30)
    print("Getting a random file from directory")
    print("=" * 30)
    print(f"Random file: {random_file}")
    print("-" * 30)
    print(f"Ground truth path: {ground_truth_path}")
    print(f"Input path: {input_path}")
    print(f"Segmentation path: {segmentation_path}")
    print("=" * 30)
    print("\n\n")  # skip 3 lines

    return ground_truth_path, input_path, segmentation_path

def load_files(ground_truth_path, input_path, segmentation_path):
    # Load ground truth file
    ground_truth_img = nib.load(ground_truth_path)
    ground_truth_data = ground_truth_img.get_fdata()

    # Load input file
    input_img = nib.load(input_path)
    input_data = input_img.get_fdata()

    # Load segmentation file
    segmentation_img = nib.load(segmentation_path)
    segmentation_data = segmentation_img.get_fdata()

    # Print
    print("=" * 30)
    print("Loading nifti files..")
    print("=" * 30)
    print(f"Ground Truth Data (from {ground_truth_path}):")
    print(f"Shape: {ground_truth_data.shape}")
    print("-" * 30)
    print(f"Input Data (from {input_path}):")
    print(f"Shape: {input_data.shape}")
    print("-" * 30)
    print(f"Segmentation Data (from {segmentation_path}):")
    print(f"Shape: {segmentation_data.shape}")
    print("=" * 30)
    print("\n\n")  # skip 3 lines

    return ground_truth_data, input_data, segmentation_data

def report_data_info(ground_truth_data, input_data, segmentation_data):
    print("=" * 30)
    print("Data Information")
    print("=" * 30)

    print("\nGround Truth Data:")
    print("-" * 30)
    print(f"Data Type: {ground_truth_data.dtype}")
    print(f"Number of Unique Values: {len(np.unique(ground_truth_data))}")

    print("\nInput Data:")
    print("-" * 30)
    print(f"Data Type: {input_data.dtype}")
    print(f"Number of Unique Values: {len(np.unique(input_data))}")

    print("\nSegmentation Data:")
    print("-" * 30)
    print(f"Data Type: {segmentation_data.dtype}")
    print(f"Number of Unique Values: {len(np.unique(segmentation_data))}")

    print("=" * 30)
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