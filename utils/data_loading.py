import nibabel as nib
import re

def get_subject_num_from_path(path):
    """
    Extracts the subject number from the given file path.
    
    Parameters:
    - path: The file path as a string.
    
    Returns:
    A string representing the subject number.
    """
    # Regular expression to match the subject number pattern
    pattern = r"sub-(\d+)"
    
    # Search the path using the pattern
    match = re.search(pattern, path)
    
    # If a match is found, return the first group (the subject number)
    if match:
        return match.group(1)
    else:
        return None

def load_nifti_data(nifti_file):
    img = nib.load(nifti_file)
    data = img.get_fdata()
    return data

