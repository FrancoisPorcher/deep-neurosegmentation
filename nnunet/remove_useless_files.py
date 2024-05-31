import os
from pathlib import Path

def remove_files(file_paths):
    for file_path in file_paths:
        file = Path(file_path)
        if file.exists() and file.is_file():
            try:
                os.remove(file)
                print(f"Removed file: {file}")
            except Exception as e:
                print(f"Failed to remove file {file}: {e}")
        else:
            print(f"File does not exist: {file}")

if __name__ == "__main__":
    # List of files to remove
    files_to_remove = [
        "/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_raw/Dataset002_dbb/imagesTr/dbb_0563_0000.nii.gz",
        "/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_raw/Dataset002_dbb/imagesTs/dbb_0563_0000.nii.gz",
        "/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_raw/Dataset002_dbb/labelsTr/dbb_0563.nii.gz",
        # Add other files to remove here
    ]

    remove_files(files_to_remove)
