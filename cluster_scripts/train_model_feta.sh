#!/bin/bash
#SBATCH -J train_nn_feta
#SBATCH -A BETHLEHEM-SL2-GPU
#SBATCH --no-requeue
#SBATCH -p ampere
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:2
#SBATCH --mail-user=rb643@cam.ac.uk
#SBATCH --mail-type=END
#SBATCH --time=21:00:00

# Load the required modules and activate the conda environment
module load miniconda/3
conda init bash
source ~/.bashrc
conda activate ~/rds/hpc-work/neurosegmentation/

# Print the current working directory and Python version for debug
pwd
python --version

# Directory paths for logs and outputs
LOGDIR="./logs/train_nn_feta/"
mkdir -p $LOGDIR
LOGFILE="$LOGDIR/train_nn_feta_$SLURM_JOB_ID.log"
ERRORFILE="$LOGDIR/train_nn_feta_$SLURM_JOB_ID.err"

# Log the job information
{
    echo "JobID: $SLURM_JOB_ID"
    echo "======"
    echo "Time: $(date)"
    echo "Running on master node: $(hostname)"
    echo "Python interpreter: $(which python)"
    echo "------------------"
} > $LOGFILE

# Set nnUNet environment variables
export nnUNet_raw="/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_raw"
export nnUNet_preprocessed="/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_preprocessed"
export nnUNet_results="/rds/project/rds-7tts6phZ4tw/deep-neurosegmentation/nnunet/nnUNet_results"

# Execute the model training, logging both stdout and stderr
nnUNetv2_train 4 3d_fullres all --npz >> $LOGFILE 2>> $ERRORFILE

# Log the end time
{
    echo "------------------"
    date
    echo "------------------"
} >> $LOGFILE
