import nibabel as nib

def load_nifti_data(nifti_file):
    img = nib.load(nifti_file)
    data = img.get_fdata()
    return data