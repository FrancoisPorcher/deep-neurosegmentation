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
To create the environment `deep_neurosegmentation`, run the following command:
```bash
conda create -n deep_neurosegmentation python=3.10 pytorch torchvision torchaudio cudatoolkit=11.3 nibabel -c pytorch -c conda-forge
```

To activate the environment, run the following command:
```bash
conda activate deep_neurosegmentation
```

