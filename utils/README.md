# Utils

This folder contains utility scripts for configuration reading and data visualization in the deep neurosegmentation project.

## Files

1. **config_reader.py**
2. **visualisation.py**

### config_reader.py

This script provides functionality to read the configuration file (`config.ini`) for setting up environment variables and paths required in the project.

#### Functions

- **read_config(config_path=None)**
  - Reads the configuration file.
  - **Parameters:**
    - `config_path` (str, optional): Path to the `config.ini` file. Defaults to a predefined path.
  - **Returns:**
    - `configparser.ConfigParser`: Configuration object.

#### Example Usage

```python
# Import the read_config function
from utils.config_reader import read_config

# Use the default path to read the configuration
config = read_config()

# Print the configuration sections and items
for section in config.sections():
    print(f"[{section}]")
    for key, value in config.items(section):
        print(f"{key} = {value}")
```

### visualisation.py

This script provides functions to select random files, load NIfTI files, and report data information including visualizations.

#### Functions

- **get_random_file_paths(base_dir)**
  - Selects random file paths from the specified base directory.
  - **Parameters:**
    - `base_dir` (str): Base directory containing 'ground_truth', 'input', and 'segmentation' subdirectories.
  - **Returns:**
    - Tuple: Paths of ground truth, input, and segmentation files.

- **load_files(ground_truth_path, input_path, segmentation_path)**
  - Loads NIfTI files from the specified paths.
  - **Parameters:**
    - `ground_truth_path` (str): Path to the ground truth file.
    - `input_path` (str): Path to the input file.
    - `segmentation_path` (str): Path to the segmentation file.
  - **Returns:**
    - Tuple: Data arrays for ground truth, input, and segmentation files.

- **report_data_info(ground_truth_data, input_data, segmentation_data)**
  - Reports information about the loaded data and visualizes the distribution of values.
  - **Parameters:**
    - `ground_truth_data` (ndarray): Data array for the ground truth.
    - `input_data` (ndarray): Data array for the input.
    - `segmentation_data` (ndarray): Data array for the segmentation.

#### Example Usage

```python
# Import necessary functions
from utils.visualisation import get_random_file_paths, load_files, report_data_info

# Base directory containing the 'ground_truth', 'input', and 'segmentation' folders
base_dir = '/path/to/base_directory'

# Get random file paths
ground_truth_path, input_path, segmentation_path = get_random_file_paths(base_dir)

# Load the files
ground_truth_data, input_data, segmentation_data = load_files(ground_truth_path, input_path, segmentation_path)

# Report data information and visualize
report_data_info(ground_truth_data, input_data, segmentation_data)
