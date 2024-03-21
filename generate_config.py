import os

# Define the base path
base_path = os.getcwd()

# Define the paths
paths = {
    "BASE_PATH": base_path,
    "DATA_PATH": f"{base_path}/data",
    "RAW_DATA_PATH": f"{base_path}/data/raw",
    "BRAINLIFE_PATH": f"{base_path}/data/raw/BrainLife",
    "DBB_PATH": f"{base_path}/data/raw/BrainLife/DBB_jakob",
    "PROJ_PATH": f"{base_path}/data/raw/BrainLife/proj-60a14ca503bcad0ad27cada9",
    "PROCESSED_DATA_PATH": f"{base_path}/data/processed",
    "MODELS_PATH": f"{base_path}/models",
    "CHECKPOINTS_PATH": f"{base_path}/models/checkpoints",
    "MODELS_CONFIGS_PATH": f"{base_path}/models/configs",
    "NOTEBOOKS_PATH": f"{base_path}/notebooks",
    "SRC_PATH": f"{base_path}/src",
    "TRAINING_PATH": f"{base_path}/src/training",
    "UTILS_PATH": f"{base_path}/utils"
}

# Generate config.py content
config_content = "\n".join([f"{key} = '{value}'" for key, value in paths.items()])

# Path to the config.py file
config_file_path = f"{base_path}/config/config.py"

# Write the paths to config.py
with open(config_file_path, "w") as config_file:
    config_file.write(config_content)

print(f"config.py generated at {config_file_path}")
