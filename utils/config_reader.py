import configparser
from pathlib import Path

def read_config(config_path=None):
    """
    Reads the configuration file.

    Parameters:
    config_path (str): The path to the config.ini file. If not provided, defaults to the specified path.

    Returns:
    configparser.ConfigParser: The configuration object.
    """
    # Default path to config.ini
    default_path = '/home/fp427/rds/rds-cam-segm-7tts6phZ4tw/deep-neurosegmentation/config.ini'
    
    # Use the provided path if given, otherwise use the default path
    path = config_path if config_path else default_path
    
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    
    # Read the configuration file
    config.read(path)
    
    return config

# Example usage within the script (can be removed or commented out if not needed)
if __name__ == "__main__":
    config = read_config()
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config.items(section):
            print(f"{key} = {value}")
