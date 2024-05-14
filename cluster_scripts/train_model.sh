#!/bin/bash
# Name of the job:
#SBATCH -J train_nnunet
#SBATCH -A BETHLEHEM-SL3-GPU
#SBATCH --no-requeue
#SBATCH -p ampere
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --mail-user=fp427@cam.ac.uk
#SBATCH --mail-type=END
#SBATCH --time=20:00:00

# Load the required modules and activate the conda environment
module load miniconda/3
conda init bash
source ~/.bashrc
conda activate neurosegmentation

# Print the current working directory and Python version
pwd
python --version

# Create directories for logs
LOGDIR=logs/
DIRPATH_EXP=$LOGDIR/$SLURM_JOB_NAME/
mkdir -p $DIRPATH_EXP

LOG=$DIRPATH_EXP/$SLURM_JOB_ID.log
ERR=$DIRPATH_EXP/$SLURM_JOB_ID.err

# Log the job information
echo -e "JobID: $SLURM_JOB_ID\n======" > $LOG
echo "Time: `date`" >> $LOG
echo "Running on master node: `hostname`" >> $LOG
echo "Python: `which python`" >> $LOG

# Print start time
echo '------------------'
date
echo '------------------'

# Set nnUNet environment variables
export nnUNet_raw=/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_raw
export nnUNet_preprocessed=/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_preprocessed
export nnUNet_results=/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_results

# Train the nnUNet model
nnUNetv2_train 1 3d_fullres all --npz

# Print end time
echo '------------------'
date
echo '------------------'
