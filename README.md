# Deep-Neurosegmentation
A Deep Learning framework to perform NeuroImaging with a Semi-Supervised Learning approach.

## Useful Links
- [Project guideline](https://docs.google.com/document/d/1340JOV0JsvpCUIeUQ3j8jZcAGy1AWgKJdzz6PUAPiP8/edit)
- [Overleaf](https://www.overleaf.com/4649694261cykwdxrwpjjc#cf931c)

## Data
The Deep-Neurosegmentation project utilizes the Distorted Brain Benchmark (DBB) dataset, which is detailed in [this article](https://www.sciencedirect.com/science/article/pii/S1053811922006024).

### Dataset Overview
- The dataset includes typically developing cohorts of children and adolescents. The raw image data for these cohorts is not publicly shared. However, we include one of the cohorts (NIHPD), identifiable through the DBB.csv file.
- For distorted brain patients (approximately 150 subjects), the raw image data is available in the `proj-` directory, originally downloaded from BrainLife.
- Synthetic domain randomized data can be found in `DBB_jakob/iteration_*` directories (1, 2, 3). Each subject has a `*_lab.nii.gz` (label mask) and `*_im.nii.gz` (synthetic brain image), both of the same dimension (182x218x182). The label masks denote tissue configuration as follows:
  - 0 = background
  - 1 = cerebrospinal fluid
  - 2 = gray matter
  - 3 = white matter
  - 4 = subcortical gray matter
  - 5 = brain stem
  - 6 = cerebellum

Data augmentation has been applied to labels and synthetic brain images to generate paired outputs, creating three iterations for a more extensive training dataset.

## Environment
To create the environment `neurosegmentation`, run the following command:
```bash
conda create -n neurosegmentation python=3.9
```

To activate the environment, run the following command:
```bash
conda activate neurosegmentation
```

To install Pytorch, run the following command:
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```
Install nnunetv2 with:

```bash
pip install nnunetv2
```

## Creation of the config file

Several python scripts access the directories of the data. To avoid hardcoding the paths, we use a config file that contains all the paths.

To create the config file `config.ini` that will be useful to get all directories, use the command:
```bash
python create_config.py
```

Note: It's possible that there is an error, and you are asked to install other libraries such as `tqdm` or `nibabel`. Install the required libraries, I will release the full environment soon.

# Data Preparation

To prepare the directory structure for your data, run the `setup_data_processed.py` script. This script creates the necessary subdirectories within the `data/processed` folder.

## Usage

### Creating Directories

To create directory structures for specific datasets, you can run the script with the desired folder names as arguments. For example:

```bash
python setup_data_processed.py mindboggle feta dbb dbb_augmented
```


This will create the following directory structure:

```bash
data/
└── processed/
    ├── mindboggle/
    │   ├── ground_truth/
    │   ├── input/
    │   └── segmentation/
    ├── feta/
    │   ├── ground_truth/
    │   ├── input/
    │   └── segmentation/
    ├── dbb/
    │   ├── ground_truth/
    │   ├── input/
    │   └── segmentation/
    └── dbb_augmented/
        ├── ground_truth/
        ├── input/
        └── segmentation/
```


### Overwriting Existing Directories

By default, the script will not overwrite existing directories. If you want to force the script to overwrite existing directories and their contents, use the `-o` or `--overwrite` flag:

```bash
python setup_data_processed.py mindboggle feta dbb dbb_augmented -o
```


This command will overwrite any existing directories for `mindboggle`, `feta`, `dbb`, and `dbb_augmented`.

### Directory Structure Explanation

The script creates the following subdirectories for each specified folder:

- `ground_truth`: Directory for ground truth data.
- `input`: Directory for input data.
- `segmentation`: Directory for segmentation data.

## Placing Raw Data

You should first place your raw data in the `data/raw` folder. After processing the data to ensure it has a homogeneous format and consistent file extensions, move the processed data to the corresponding subdirectories in the `data/processed` folder.

### Example

To create a directory structure for the `mindboggle` and `feta` datasets without overwriting existing directories, run:

```bash
python setup_data_processed.py mindboggle feta
```


To create and overwrite the directory structure for all four datasets (`mindboggle`, `feta`, `dbb`, `dbb_augmented`), run:

```bash
python setup_data_processed.py mindboggle feta dbb dbb_augmented -o
```


By following these instructions, you can set up the directory structure needed for data preprocessing efficiently.




# nnUNet

## Set up the data structure for nnUNet

To setup nnUnetV2 data structure, go in the nnunet folder and run
```bash
cd nnunet
python setup_nnunet.py
```


To setup nnUNetV2 data structure plus specific datasets (MindBoggle, DBB, etc.), run the following command:
```bash
python setup_nnunet.py --mindboggle --dbb
```

## Setting up the environment variables for nnunet

Before running any command that uses the nnunet package, you need to set up the following environment variables.

These variables have been setup by the `setup_nnunet.py` script just before. Check the `config.ini` file to see the values. At the moment I am writing the readme, the values are:

```bash
export nnUNet_raw=/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_raw

export nnUNet_preprocessed=/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_preprocessed

export nnUNet_results=/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_results
```

(Optional): To check if the environment variables have been set up correctly, run the following command:
```bash
echo $nnUNet_raw
echo $nnUNet_preprocessed
echo $nnUNet_results
```

(Optional): These variables are temporary and will be lost when you close the terminal. If you want to keep these variables, you can add them to your `.bashrc` or `.bash_profile` file, and each time you open a terminal, they will be set up automatically. To do this, run the following commands:

```bash
echo "export nnUNet_raw=/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_raw" >> ~/.bashrc
echo "export nnUNet_preprocessed=/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_preprocessed" >> ~/.bashrc
echo "export nnUNet_results=/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_results" >> ~/.bashrc
```

## Plan and Process for nnUNet

Now that your data has been set up in the right format (.nii or .nii.gz files), you still need to prepare them to be compatible for the nnUNetv2 format.

You can run the following command, where you repace `DATASET_ID` with the corresponding dataset id.

```
nnUNetv2_plan_and_preprocess -d DATASET_ID --verify_dataset_integrity
```

The corresponding I am using is:

- 1: MindBoggle
- 2: DBB
- 3: DBB_augmented
- 4: Feta

Example with MindBoggle:
- I replace -d with 1 for the MindBoggle associated id.
- I also add `-c 3d_fullres` because I only use the 3D CNN, no need to train the 2D cnn nor the cascade.

```bash
nnUNetv2_plan_and_preprocess -d 1 --verify_dataset_integrity -c 3d_fullres
```

## Training nnUNet

To train the nnUNet model, you can send a SLURM job with the `train_model.sh` script in the `./cluster_scripts` folder.

You can run the following command:

```bash
cd cluster_scripts
sbatch train_model.sh
```

By default: the `train_model.sh` script will train the model on the MindBoggle dataset with the 3d_fullres network and all folds.

You should edit this file to train on the dataset you want. 

Here are the guidelines:

This `train_model.sh` bash script will call the `nnUNetv2_train` command with the corresponding dataset, network, and fold.

The general command is:

```bash
nnUNetv2_train DATASET_ID NETWORK FOLD
```

Example:
On the MindBoggle dataset, with the 3d_fullres network and training on all data:
```bash
nnUNetv2_train 1 3d_fullres all
```

If you want to save the softmax outputs during the final validation (useful for ensembling or detailed analysis), you can add the --npz flag:

```bash
nnUNetv2_train 1 3d_fullres all --npz
```

## Inference with nnUNet

To perform inference with nnUNet, you can run the following command:

```bash
nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_ID -c CONFIGURATION
```

If you want to save the probabilities:

```bash
nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_ID -c CONFIGURATION --save_probabilities
```

Example:
With the MindBoggle dataset (dataset ID 1) and 3D full resolution U-Net:

```bash
nnUNetv2_predict -i /path/to/input_folder -o /path/to/output_folder -d 1 -c 3d_fullres --save_probabilities
```

## Evaluation with nnUNet

The general command for evaluation is:

```bash
nnUNetv2_evaluate_folder -ref REFERENCE_FOLDER -pred PREDICTION_FOLDER -json OUTPUT_JSON -use_labels LABELS
```

Example with MindBoggle dataset (dataset ID 1):

```bash
nnUNetv2_evaluate_folder -ref /path/to/reference_folder -pred /path/to/prediction_folder -json /path/to/output.json -use_labels 1 2 3 4 5 6
```